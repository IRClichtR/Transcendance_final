const createElement = (tagName, attributes, ...children) => {
	const prop = document.createElement(tagName);

	for (const [key, value] of Object.entries(attributes || {})) {
		prop.setAttribute(key, value);
	}

	prop.append(...children);

	prop.setStyle = (styles) => {
		Object.assign(prop.style, styles);
		return prop;
	};

	prop.appendText = (text) => {
		prop.append(text);
		return prop;
	};

	prop.on = (eventType, eventHandler, options) => {
		prop.addEventListener(eventType, eventHandler, options);
		return prop;
	};

	return prop;
};

export default createElement;
