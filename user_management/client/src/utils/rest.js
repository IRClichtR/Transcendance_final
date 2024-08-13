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
		console.log('updateUser user.entries :\n');

		for (let [key, value] of user.entries()) {
			console.log(key, ' : ', value);
		}

		console.log('\n');

		const response = await rest.patch('/user/update/', {
			body: user,
		});
		console.log('updateUser response : ', response);
		console.log('\n');

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

const updatePassword = async ({ confirm_new_password, new_password, old_password }) => {
	try {
		const response = await rest
			.put('/user/password/', {
				json: { confirm_new_password, new_password, old_password },
			})
			.json();
		return response;
	} catch (error) {
		console.error('Failed to update password:', error);
		throw new Error('Failed to update password');
	}
};

export { rest, getMe, updateUser, updatePassword, getProfilePic };
