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
			const response = await getMe({ signal });

			if (response.image?.link) {
				this.link = response.image.link;
				console.log('response.image.link: ', this.link);
				return response;
			} else if (response?.profile_picture) {
				this.link = 'http://localhost:8000' + response.profile_picture;
				console.log('response.profile_picture: ', this.link);
				return response;
			}

			const storedAvatar = this.getStoredAvatarSrc(response.email);
			if (storedAvatar) {
				this.link = storedAvatar;
			} else {
				const random = this.getRandomAvatarSrc();
				this.storeAvatarSrc(response.email, random);
				this.link = random;
			}
			return response;
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

	storeAvatarSrc = (email, src) => {
		if (!email || typeof email !== 'string') {
			throw new Error(
				'Unable to store avatar without an email, got: ' + email
			);
		}
		if (!src || typeof src !== 'string') {
			throw new Error(
				'Unable to store avatar without a src, got: ' + src
			);
		}
		const avatars = localStorage.getItem('avatars');
		const parsed = avatars ? JSON.parse(avatars) : {};
		parsed[email] = src;
		const stringified = JSON.stringify(parsed);
		localStorage.setItem('avatars', stringified);
	};

	getStoredAvatarSrc = (email) => {
		if (!email || typeof email !== 'string') {
			throw new Error(
				'Unable to store avatar without an email, got: ' + email
			);
		}
		const avatars = localStorage.getItem('avatars');
		const parsed = avatars ? JSON.parse(avatars) : {};
		return parsed[email] || '';
	};

	// * Update Password
	async updatePassword(event) {
		event.preventDefault();
		const formData = new FormData(event.target);
		const currentPassword = formData.get('currentPassword');
		const newPassword = formData.get('newPassword');
		const confirmPassword = formData.get('confirmPassword');

		if (newPassword !== confirmPassword) {
			console.error('New password and confirm password do not match');
			alert('New password and confirm password do not match');
			return;
		}

		try {
			const response = await updatePassword({
				currentPassword,
				newPassword,
			});
			console.log('Password updated successfully:', response);
			alert('Password updated successfully');
		} catch (error) {
			console.error('Error updating password:', error);
			alert('Error updating password');
		}
	}

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
												<div
													class="card-header text-bg-dark"
												>
													Hello,
													${user.displayname
														? user.displayname
														: user.first_name}!
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
															for="currentPassword"
															class="form-label"
															>Current
															Password</label
														>
														<input
															type="password"
															class="form-control"
															id="currentPassword"
															name="currentPassword"
															required
														/>
													</div>
													<div class="col-12">
														<label
															for="newPassword"
															class="form-label"
															>New Password</label
														>
														<input
															type="password"
															class="form-control"
															id="newPassword"
															name="newPassword"
															required
														/>
													</div>
													<div class="col-12">
														<label
															for="confirmPassword"
															class="form-label"
															>Confirm
															Password</label
														>
														<input
															type="password"
															class="form-control"
															id="confirmPassword"
															name="confirmPassword"
															required
														/>
													</div>
													<div class="col-12">
														<button
															type="submit"
															class="btn btn-primary"
														>
															Change Password
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
