import { Task } from '@lit/task';
import { LitElement, html, css } from 'lit';
import { getMe, updateUser, getProfilePic } from '../../utils/rest.js';
import { query } from 'lit/decorators/query.js';

export class SettingsComponent extends LitElement {
	static properties = {
		user: {},
		link: { type: String },
		profilePicture: { type: String },
		previewSrc: { type: String },
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
		this.profilePicture = '';
		this.previewSrc = '';
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

	updateUserInfo = async (event) => {
		event.preventDefault();
		const formData = new FormData(event.target);

		console.log('updateUserInfo-formData.entries :\n');
		for (let [key, value] of formData.entries()) {
			console.log(key, ' : ', value);
		}
		console.log('\n');

		const newUsername = formData.get('username');
		const regex = /^[a-zA-Z0-9]+$/;
		const regexAlpha = /^[a-zA-Z]+$/;

		const newFirstname = formData.get('first_name');
		const newLastname = formData.get('last_name');

		if (!regex.test(newUsername)) {
			alert('The username must contain alphanumeric character only.');
			return;
		}
		if (!regexAlpha.test(newFirstname) || !regexAlpha.test(newLastname)) {
			alert('The firstname and lastname must contain alphabetic character only.');
			return;
		}

		try {
			const response = await updateUser(formData);

			console.log('updatUserInfo response.entries :\n');
			for (let [key, value] of formData.entries()) {
				console.log(key, ' : ', value);
			}
			console.log('\n');

			location.reload();

		} catch (error) {
			console.error('Error updating user:', error);
		}
	};

	previewPhoto = (event) => {
		const input = event.target;
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
																name="first_name"
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
																name="last_name"
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
																value="${user?.username
																	? user.username
																	: user.displayname}"
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
														<div class="col-12">
															<button
																type="submit"
																class="btn btn-primary ${user.login
																	? 'disabled'
																	: ''}"
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
