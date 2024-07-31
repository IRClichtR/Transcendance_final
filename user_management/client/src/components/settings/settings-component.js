import { Task } from '@lit/task';
import { LitElement, html, css } from 'lit';
import { getMe, updateUser, getProfilePic } from '../../utils/rest.js';
import { query } from 'lit/decorators/query.js';

export class SettingsComponent extends LitElement {
	static properties = {
		user: {},
		link: { type: String },
		profilePicture: { type: String },
	};

	_userTask = new Task(this, {
		task: async ([user], { signal }) => {
			const response = await getMe({ signal });
			console.log('Ky got user:', response);
			if (response.image?.link) {
				this.link = response.image.link;
				return response;
			}
			const storedAvatar = await this.getStoredAvatarSrc(response.email);
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
		this.profilePicture = '';
		this.previewSrc = '';
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

	getStoredAvatarSrc = async (email) => {
		if (!email || typeof email !== 'string') {
			throw new Error(
				'Unable to store avatar without an email, got: ' + email
			);
		}
		const storedProfilePicture = await getProfilePic();
		if (storedProfilePicture) return storedProfilePicture;
		const avatars = localStorage.getItem('avatars');
		const parsed = avatars ? JSON.parse(avatars) : {};
		return parsed[email] || '';
	};

	updateUserInfo = async (event) => {
		event.preventDefault();
		const formData = new FormData(event.target);
		console.log('formData => ', [...formData.entries()]);

		try {
			const response = await updateUser(formData);
			console.log('User updated successfully =>', response);
			// Optionally, update the user property to reflect changes
			this.user = response;
			console.log('this.user::::: ', this.user);
		} catch (error) {
			alert('Please provide a valid email.', error);
			console.error('Error updating user:', error);
		}
	};

	previewPhoto = (event) => {
		const input = event.target;
		console.log('input =====> ', input);
		const file = input.files;
		if (file) {
			const fileReader = new FileReader();
			const preview = this.shadowRoot.getElementById('selectedImage');
			fileReader.onload = (event) => {
				preview.setAttribute('src', event.target.result);
			};
			fileReader.readAsDataURL(file[0]);
		}
	};

	render() {
		return this._userTask.render({
			pending: () => html`<p>Loading settings...</p>`,
			complete: (user) => html`
				<div class="container container-xxl h-100">
					<section class="bg-light py-3 py-md-5 py-xl-8">
						<div class="container">
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
															src="${this.link}"
															class="img-fluid rounded-circle"
															alt="${user.displayname
																? user.displayname
																: user.first_name}"
														/>
													</div>
													<h5
														class="text-center mb-1"
													>
														${user.displayname
															? user.displayname
															: user.first_name +
																' ' +
																user.last_name}
													</h5>
													<div
														class="d-grid m-0"
													></div>
												</div>
											</div>
										</div>
									</div>
								</div>
								<div class="col-12 col-lg-8 col-xl-9">
									<div class="card widget-card shadow-sm">
										<div class="card-body">
											<div
												class="tab-content"
												id="profileTabContent"
											>
												<div
													class="tab-pane fade show active"
													id="overview-tab-pane"
													role="tabpanel"
													aria-labelledby="overview-tab"
													tabindex="0"
												>
													<h5
														style="text-decoration: underline"
														class="mb-3 text-lg"
													>
														Settings
													</h5>
													<form
														@submit=${this
															.updateUserInfo}
														class="row gy-3 gy-xxl-4"
													>
														<div class="col-12">
															<div
																class="row gy-2 pt-4"
															>
																<label
																	class="col-12 form-label m-0"
																	>Profile
																	Image</label
																>
																<div
																	class="col-12"
																>
																	<div>
																		<div
																			class=" d-flex "
																		>
																			<img
																				id="selectedImage"
																				src=${this
																					.link
																					? this
																							.link
																					: 'https://bootdey.com/img/Content/avatar/avatar1.png'}
																				alt="example placeholder"
																				style="width: 300px;"
																			/>
																		</div>
																		<div
																			class="d-flex"
																		>
																			<div
																				data-mdb-ripple-init
																				class=""
																			>
																				<label
																					class="badge bg-dark form-label text-white mb-4"
																					for="customFile1"
																					>Upload
																					file</label
																				>
																				<input
																					name="profile_picture"
																					type="file"
																					class="form-control d-none"
																					id="customFile1"
																					@change=${this
																						.previewPhoto}
																				/>
																			</div>
																		</div>
																	</div>
																</div>
															</div>
														</div>
														<div
															class="col-12 col-md-6"
														>
															<label
																for="inputFirstName"
																class="form-label"
																>First
																Name</label
															>
															<input
																type="text"
																class="form-control"
																id="inputFirstName"
																name="first_Name"
																value="${user.first_name}"
															/>
														</div>
														<div
															class="col-12 col-md-6"
														>
															<label
																for="inputLastName"
																class="form-label"
																>Last
																Name</label
															>
															<input
																type="text"
																class="form-control"
																id="inputLastName"
																name="last_Name"
																value="${user.last_name}"
															/>
														</div>
														<div
															class="col-12 col-md-6"
														>
															<label
																for="inputUsername"
																class="form-label"
																>Username</label
															>
															<input
																type="text"
																class="form-control"
																id="inputUsername"
																name="username"
																value="${user.username}"
															/>
														</div>
														<div
															class="col-12 col-md-6"
														>
															<label
																for="inputEmail"
																class="form-label"
																>Email</label
															>
															<input
																type="email"
																class="form-control"
																id="inputEmail"
																name="email"
																value="${user.email}"
															/>
														</div>
														<div
															class="col-12 col-md-6"
														>
															<label
																for="inputConfirmEmail"
																class="form-label"
																>Confirm
																Email</label
															>
															<input
																type="email"
																class="form-control"
																id="inputConfirmEmail"
																value="${user.email}"
															/>
														</div>
														<div class="col-12">
															<button
																type="submit"
																class="btn btn-primary"
															>
																Save Changes
															</button>
														</div>
													</form>
												</div>
											</div>
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
customElements.define('settings-component', SettingsComponent);
