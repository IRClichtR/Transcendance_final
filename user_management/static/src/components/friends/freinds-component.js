import { Task } from '@lit/task';
import { LitElement, html, css } from 'lit';
import { getMe } from '../../utils/rest.js'; // Assuming getMe is the function to get user details

export class FreindsComponent extends LitElement {
	static properties = {
		user: { type: Object },
		link: { type: String },
		friends: { type: Array },
		myFriends: { type: Array },
	};

	constructor() {
		super();
		this.link = '';
		this.friends = [];
		this.myFriends = this.loadFriendsFromStorage();
		this.fetchFriends();
	}

	async fetchFriends() {
		try {
			const response = await fetch('/user');
			if (response.ok) {
				const data = await response.json();
				this.friends = data;
			} else {
				console.error('Failed to fetch friends');
			}
		} catch (error) {
			console.error('Error fetching friends:', error);
		}
	}

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

	saveFriendsToStorage() {
		localStorage.setItem('myFriends', JSON.stringify(this.myFriends));
	}

	loadFriendsFromStorage() {
		const storedFriends = localStorage.getItem('myFriends');
		return storedFriends ? JSON.parse(storedFriends) : [];
	}

	handleAddFriend(friend) {
		if (!this.myFriends.some((f) => f.email === friend.email)) {
			this.myFriends = [...this.myFriends, friend];
			this.saveFriendsToStorage();
			this.requestUpdate(); // Ensure the component updates
		}
	}

	handleRemoveFriend(friend) {
		this.myFriends = this.myFriends.filter((f) => f.email !== friend.email);
		console.log('myFriends after remove::::::::', this.myFriends);
		this.saveFriendsToStorage();
		this.requestUpdate(); // Ensure the component updates
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
			pending: () => html`<p>Loading friends...</p>`,
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
															src="${this.link}"
															class="img-fluid rounded-circle"
															alt="${user.first_name}"
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
									<div class="card widget-card shadow-sm p-3">
										<div class="row align-items-center">
											<h5
												style="text-decoration: underline;"
												class=""
											>
												Add Friends
											</h5>
											<div class="py-6">
												<div class="row">
													${this.friends.map(
														(friend) =>
															friend.first_name ===
															user.first_name
																? ``
																: html`
																		<div
																			class="col-lg-4 col-12"
																		>
																			<div
																				class="card mt-5 rounded-3"
																			>
																				<div
																					class="card-body d-flex justify-content-between"
																				>
																					<div>
																						<h4
																							class="mb-1"
																						>
																							${friend.first_name +
																							' ' +
																							friend.last_name}
																						</h4>
																						<span
																							>${this.checkIfOnline(
																								friend
																							)
																								? 'Online'
																								: 'Offline'}
																						</span>
																					</div>
																					<div
																						class="pl-4"
																					>
																						<button
																							@click=${() =>
																								this.handleAddFriend(
																									friend
																								)}
																							class="btn btn-sm btn-outline-success mr-2 mb-2"
																							style="height: 30px; width: 100px;"
																						>
																							Add
																						</button>
																					</div>
																				</div>
																			</div>
																		</div>
																	`
													)}
												</div>
											</div>
											<h5
												style="text-decoration: underline;"
												class="mt-5"
											>
												My Friends
											</h5>
											<div class="py-6">
												<div class="row">
													${this.myFriends.map(
														(friend) => friend.first_name  === user.first_name ?
                                                            `` :
                                                            html`
															<div
																class="col-lg-4 col-12"
															>
																<div
																	class="card mt-5 rounded-3"
																>
																	<div
																		class="card-body d-flex justify-content-between"
																	>
																		<div>
																			<h4
																				class="mb-1"
																			>
																				${friend.first_name +
																				' ' +
																				friend.last_name}
																			</h4>
																			<span
																				>${this.checkIfOnline(
																					friend
																				)
																					? 'Online'
																					: 'Offline'}
																			</span>
																		</div>
																		<button
																			@click=${() =>
																				this.handleRemoveFriend(
																					friend
																				)}
																			class="btn btn-sm btn-outline-danger"
																			style="height: 30px;"
																		>
																			Remove
																		</button>
																	</div>
																</div>
															</div>
														`
													)}
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

customElements.define('freinds-component', FreindsComponent);
