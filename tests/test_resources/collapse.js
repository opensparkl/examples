// up arrow
var HIDE_ARROW = '&#x25B2;'
// down arrow
var RESET_ARROW = '&#x25BC;'


function get_div_parent(element){
	var parent = element.parentNode
	while (parent.tagName != 'DIV'){
		parent = parent.parentNode
	}
	return parent
}


function click_me(button){
	if (button.closed){
		reset(button)
	}

	else {
		hide(button)
	}
}


function change_display(element, child_tag, new_style){
	var div = get_div_parent(element)
	var children = div.getElementsByTagName(child_tag)

	for (i=0; i < children.length; i ++){
		children[i].style.display = new_style
	}
}


function hide(button){
	change_display(button, 'div', 'none')
	button.innerHTML = RESET_ARROW
	button.closed = true
}


function reset(button){
	change_display(button, 'div', 'block')
	button.innerHTML = HIDE_ARROW
	button.closed = false
}