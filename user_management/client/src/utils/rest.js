import ky from 'https://esm.sh/ky@1';

const rest = ky.extend({
	mode: 'same-origin',
	timeout: 30_000,
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
	return rest.get('/user/me', options).json();
};

const updateUser = async (user) => {
	try {
		const response = await ky
			.put('/user/update', {
				json: user,
			})
			.json();
		return response;
	} catch (error) {
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

export { rest, getMe, updateUser, updatePassword };
