"""
Author <miklos@sparkl.com> Miklos Duma
Copyright 2018 SPARKL Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Utility functions for matching SPARKL events.
"""


def get_short_name(full_path):
    """
    Returns the short name of an operation or service,
    without the full path to it.
    """
    return full_path.rsplit('/')[-1]


def match_fields(exp_fields, fields):
    """
    Check field names and values match the expected ones.
        - exp_fields:
            A list of dictionaries with field name/value pairs.
        - fields:
            SPARKL event fields as returned by the listener.
            [
                {'attr': {'name':'n', 'value':3}},
                {'attr': {'name': 'div', 'value':2}}]
    """
    # Reformat event fields to contain only name and value. If value is not
    # given (in case of FLAG fields), value is None.
    fields = [{field['attr']['name']: field['attr']['value']}
              if 'value' in field['attr']
              else {field['attr']['name']: None}
              for field in fields]

    return exp_fields == fields


def match_state(exp_state, states):
    """
    Matches state values.
        - exp_state:
            A dictionary of expected state values, where
            the key is the state name, the value the expected state.
        - states:
            The state content of the state change event.
    Returns either True or False based on the match.
    """
    for exp_state_name, exp_state_val in exp_state.items():
        if exp_state_name not in states:
            return False

        if states[exp_state_name] != exp_state_val:
            return False

    return True


def get_state_values(event, event_tag='new'):
    """
    Retrieves the states from a state change event and
    returns them as a dictionary of state name/state value pairs.

        - event:
            The SPARKL event as returned by `sparkl listen`.
        - event_tag:
            Either `old` or `new` (default). Decides whether
            the function returns the current (new) state values
            or the ones before the state change (old).
    """
    return_dict = dict()

    for content in event['content']:
        if content['tag'] == event_tag:
            for key, value in content['attr'].items():
                return_dict[key] = value

    return return_dict


def match_state_change(event, service, exp_old=None, exp_new=None):
    """
    Matches a state change event.
        - event:
            The SPARKL event as returned by `sparkl listen`.
        - service:
            The SPARKL service we listen to for state changes.
        - exp_old (optional):
            The expected state values before the state change.
        - exp_new:
            The expected state values after the state change.

    Returns True or False.
    """
    event_tag = event['tag']

    if event_tag != 'state_change':
        return False

    service_name = get_short_name(event['attr']['service'])

    if service_name != service:
        return False

    if exp_old:
        old_state = get_state_values(event, event_tag='old')

        if not match_state(exp_old, old_state):
            return False

    if exp_new:
        new_state = get_state_values(event)

        if not match_state(exp_new, new_state):
            return False

    return True


def match_event_with_field(event, event_type, name, exp_fields=None):
    """
    Matches the event against a dictionary of expected
    values comprising an operation name and field values.
    """
    event_tag = event['tag']

    if event_tag != event_type:
        return False

    event_name = get_short_name(event['attr'][event_tag])

    if event_name != name:
        return False

    if exp_fields:
        fields = event['content']
        return match_fields(exp_fields, fields)

    return True
