function click_me(button){
	var klass = button.getAttribute('class')

	if (klass == 'pressed'){
		reset(button)
	}

	else {
		hide(button)
	}
}


function hide(button){
	var div = button.parentNode
	var div_children = div.getElementsByTagName('div')
	button.to_reset = []

	for (i=0; i < div_children.length; i ++){
		div_children[i].style.display = 'none'
		button.to_reset.push(div_children[i])
	}
	button.setAttribute('class', 'pressed')
	button.innerHTML = '&#x25BC;'
}

function reset(button){
	for (i=0; i < button.to_reset.length; i ++){
		button.to_reset[i].style.display = 'block'
	}
	button.removeAttribute('class')
	button.to_reset = []
	button.innerHTML = '&#x25B2;'
}