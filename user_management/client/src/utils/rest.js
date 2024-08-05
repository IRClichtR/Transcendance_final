import ky from 'https://esm.sh/ky@1';

const getCookies = () => {
	return Object.fromEntries(
		document.cookie
			.split('; ')
			.map((v) => v.split(/=(.*)/s).map(decodeURIComponent))
	);
};

const csrfToken = getCookies().csrftoken;

const rest = ky.extend({
	mode: 'same-origin',
	timeout: 30_000,
	headers: {
		'X-CSRFToken': csrfToken,
	},
	hooks: {
		afterResponse: [
			async (request, options, response) => {
				if (response.status === 401) {
					location.assign(
						'/login?next=' + encodeURIComponent(location.pathname)
					);
				}
			},
		],
	},
});

const getMe = (options = {}) => {
	const response = rest.get('/user/me', options).json();
	return response;
};

const updateUser = async (user) => {
	try {
		console.log('New user info => ', user);
		const response = await rest.patch('/user/update/', {
			body: user,
		});
		return response;
	} catch (error) {
		if (error.response) {
			console.log('Error details (response) => ', error.response);
			console.log('Error status => ', error.response.status);
			console.log('Error data => ', await error.response.json());
		} else if (error.request) {
			console.log('Error details (request) => ', error.request);
		} else {
			console.log('Error message => ', error.message);
		}
		throw new Error('Failed to update user');
	}
};

const getProfilePic = async (user) => {
	try {
		const response = await getMe();
		return response;
	} catch (error) {
		console.log('error: ', error);
		throw new Error('Failed to update user');
	}
};

const updatePassword = async ({ currentPassword, newPassword }) => {
	try {
		const response = await ky
			.put('/user/password', {
				json: { currentPassword, newPassword },
			})
			.json();
		return response;
	} catch (error) {
		console.error('Failed to update password:', error);
		throw new Error('Failed to update password');
	}
};

export { rest, getMe, updateUser, updatePassword, getProfilePic };
