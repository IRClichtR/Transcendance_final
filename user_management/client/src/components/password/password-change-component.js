import { Task } from '@lit/task';
import { LitElement, html, css } from 'lit';
import { getMe, updatePassword } from '../../utils/rest.js';

export class PasswordChangeComponent extends LitElement {
	static properties = {
		user: {},
		link: { type: String },
	};

	_userTask = new Task(this, {
		task: async ([user], { signal }) => {
			const me = await getMe({ signal });
	
			const id = me.id.toString();
	
			if (me.image?.link) {
				this.link = me.image.link;
				return me;
			} else if (me.profile_picture) {
				this.link = me.profile_picture;
				this.storeAvatarSrc(id, this.link);
				return me;
			}
	
			const storedAvatar = await this.getStoredAvatarSrc(id);
			if (storedAvatar) {
				this.link = storedAvatar;
			} else {
				const random = this.getRandomAvatarSrc();
				this.storeAvatarSrc(id, random);
				this.link = random;
			}
	
			return me;
		},
		args: () => [this.user],
	});

	static get styles() {
		const { cssRules } = document.styleSheets[0];
		const globalStyle = css([
			Object.values(cssRules)
				.map((rule) => rule.cssText)
				.join('\n'),
		]);
		return [globalStyle, css``];
	}

	constructor() {
		super();
		this.link = '';
	}

	getRandomAvatarSrc = () => {
		const randomSrc = Math.floor(Math.random() * this.images.length);
		return this.images[randomSrc];
	};

	storeAvatarSrc = (id, src) => {
		if (!id || typeof id !== 'string') {
			throw new Error(
				'Unable to store avatar without a user ID, got: ' + id
			);
		}
		if (!src || typeof src !== 'string') {
			throw new Error(
				'Unable to store avatar without a src, got: ' + src
			);
		}
		const avatars = localStorage.getItem('avatars');
		const parsed = avatars ? JSON.parse(avatars) : {};
		parsed[id] = src;
		const stringified = JSON.stringify(parsed);
		localStorage.setItem('avatars', stringified);
	};
	
	getStoredAvatarSrc = async (id) => {
		if (!id || typeof id !== 'string') {
			throw new Error(
				'Unable to store avatar without a user ID, got: ' + id
			);
		}
		const avatars = localStorage.getItem('avatars');
		const parsed = avatars ? JSON.parse(avatars) : {};
		return parsed[id] || '';
	};

	// * Update Password
	async updatePassword(event) {
		console.log('event: ', event);
		event.preventDefault();
		const formData = new FormData(event.target);
		console.log('formData: ', formData);
		const old_password = formData.get('old_password');
		console.log('old_password: ', old_password);
		const new_password = formData.get('new_password');
		console.log('new_password: ', new_password);
		const confirm_new_password = formData.get('confirm_new_password');
		console.log('confirm_new_password: ', confirm_new_password);

		if (new_password !== confirm_new_password) {
			console.error('New password and confirm password do not match');
			alert('New password and confirm password do not match');
			return;
		}

		if (old_password == new_password)
		{
			console.error('New password and ol password match');
			alert('New password and old password match. Please choose an other password');
			return;
		}

		try {
			const response = await updatePassword({
				old_password,
				new_password,
				confirm_new_password,
			});
			console.log('Password updated successfully:', response);

			// Déconnecter l'utilisateur
			alert('Password updated successfully. You have been logged out. Please log in again.');
			window.location.href = '/logout'; // Rediriger vers la page de connexion

		} catch (error) {
			console.error('Error updating password:', error);
			alert('Error updating password');
		}
	}

	checkIfOnline = (user) => {
		const hour = 60 * 60 * 1000;
		const lastLoginDate = new Date(user.last_login);
		const now = new Date();
		const timeLogedIn = now - lastLoginDate;
		timeLogedIn < hour ? (this.isOnline = true) : (this.isOnline = false);
		return this.isOnline;
	};

	render() {
		return this._userTask.render({
			pending: () => html`<p>Loading password...</p>`,
			complete: (user) => html`
				<div class="container container-fluid h-100">
					<section class="bg-light py-3 py-md-5 py-xl-8 shadow-sm">
						<div class="container-xxl container-fluid">
							<div class="row gy-4 gy-lg-0">
								<div class="col-12 col-lg-4 col-xl-3">
									<div class="row gy-4">
										<div class="col-12">
											<div
												class="card widget-card shadow-sm"
											>
												<div class="card-header">
													<p>
														Hello,
														${user.first_name}!
														<span
															>${this.checkIfOnline(
																user
															)
																? 'Online'
																: 'Offline'}
														</span>
													</p>
												</div>
												<div class="card-body">
													<div
														class="text-center mb-3"
													>
														<img
															src="${this.link
																? this.link
																: 'https://bootdey.com/img/Content/avatar/avatar1.png'}"
															class="img-fluid rounded-circle"
															alt="${user.displayname}"
														/>
													</div>
													<div
														class="card-body border-dark shadow-sm"
													>
														<h5
															class="text-center mb-1"
														>
															${user.displayname
																? user.displayname
																: user.first_name +
																	' ' +
																	user.last_name}
														</h5>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
								<div class="col-12 col-lg-8 col-xl-9">
									<div class="card widget-card shadow-sm">
										<div class="card-body">
											<div
												class="tab-pane fade show active"
												id="overview-tab-pane"
												role="tabpanel"
												aria-labelledby="overview-tab"
												tabindex="0"
											></div>
											<h5
												style="text-decoration: underline"
												class="mb-3 text-lg"
											>
												Password Reset
											</h5>
											<form
												@submit=${this.updatePassword}
											>
												<div class="row gy-3 gy-xxl-4">
													<div class="col-12">
														<label
															for="old_password"
															class="form-label"
															>Current
															Password</label
														>
														<input
															type="password"
															class="form-control"
															id="old_password"
															name="old_password"
															required
														/>
													</div>
													<div class="col-12">
														<label
															for="new_password"
															class="form-label"
															>New Password</label
														>
														<input
															type="password"
															class="form-control"
															id="new_password"
															name="new_password"
															required
														/>
													</div>
													<div class="col-12">
														<label
															for="confirm_new_password"
															class="form-label"
															>Confirm
															Password</label
														>
														<input
															type="password"
															class="form-control"
															id="confirm_new_password"
															name="confirm_new_password"
															required
														/>
													</div>
													<div class="col-12">
                                                        <button
                                                            type="submit"
                                                            class="btn btn-primary ${user.login
                                                                ? 'disabled'
                                                                : ''}"
                                                        >
                                                            Save Password
                                                        </button>
													</div>
												</div>
											</form>
										</div>
									</div>
								</div>
							</div>
						</div>
					</section>
				</div>
			`,
			error: (e) => html`<p>Error: ${e}</p>`,
		});
	}
}
customElements.define('password-change-component', PasswordChangeComponent);
