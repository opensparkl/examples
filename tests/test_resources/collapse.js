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


function change_button(button){
	if (button.hasAttribute('class')){
		button.removeAttribute('class')
		button.innerHTML = HIDE_ARROW
	
	} else {
		button.setAttribute('class', 'visible')
		button.innerHTML = RESET_ARROW
	}
}


function change_children(children){
	for (i=0; i < children.length; i ++){

		if (children[i].hasAttribute('class')){
			children[i].removeAttribute('class')
		
		} else {
			children[i].setAttribute('class', 'visible')
		}
	}
}


function click_me(button){
	change_button(button)

	var div = get_div_parent(button)
	var children = div.children
	change_children(children)
}