import { Task } from '@lit/task';
import { LitElement, html, css } from 'lit';
import { getMe, getTournamentData } from '../../utils/rest.js';

export class DashboardComponent extends LitElement {
	static properties = {
		user: {},
		userTournametData: {},
		link: { type: String },
		data: { type: Array },
		isOnline: { type: Boolean },
	};

	_userTask = new Task(this, {
		task: async ([user], { signal }) => {
			const response = await getMe({ signal });
			this.tournamentData = await getTournamentData(response);
			console.log('this.tournamentData:', this.tournamentData);
			if (response.image?.link) {
				this.link = response.image.link;
				return response;
			} else if (response?.profile_picture) {
				this.link = response.profile_picture;
				return response;
			} else {
				const storedAvatar = this.getStoredAvatarSrc(response.email);
				if (storedAvatar) {
					this.link = storedAvatar;
				} else {
					const random = this.getRandomAvatarSrc();
					this.storeAvatarSrc(response.email, random);
					this.link = random;
				}
				return response;
			}
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
		this.data = [];
		this.isOnline = false;
		this.images = [
			'https://cdn-icons-png.flaticon.com/128/8034/8034504.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034557.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034553.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034539.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034535.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034525.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034520.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034518.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034514.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034492.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034484.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034478.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034474.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034468.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034455.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034451.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034448.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034441.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034439.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034561.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034500.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034545.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034530.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034508.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034444.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034550.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034489.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034464.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034459.png',
			'https://cdn-icons-png.flaticon.com/128/8034/8034559.png',
		];
	}

	getRandomAvatarSrc = () => {
		const randomSrc = Math.floor(Math.random() * this.images.length);
		return this.images[randomSrc];
	};

	storeAvatarSrc = (email, src) => {
		if (!email || typeof email !== 'string') {
			throw new Error('Unable to store avatar without an email, got: ' + email);
		}
		if (!src || typeof src !== 'string') {
			throw new Error('Unable to store avatar without a src, got: ' + src);
		}
		const avatars = localStorage.getItem('avatars');
		const parsed = avatars ? JSON.parse(avatars) : {};
		parsed[email] = src;
		const stringified = JSON.stringify(parsed);
		localStorage.setItem('avatars', stringified);
	};

	getStoredAvatarSrc = (email) => {
		if (!email || typeof email !== 'string') {
			throw new Error('Unable to store avatar without an email, got: ' + email);
		}
		const avatars = localStorage.getItem('avatars');
		const parsed = avatars ? JSON.parse(avatars) : {};
		return parsed[email] || '';
	};

	checkIfOnline = (user) => {
		const hour = 60 * 60 * 1000;
		const lastLoginDate = new Date(user.last_login);
		const now = new Date();
		const timeLogedIn = now - lastLoginDate;

		console.log(timeLogedIn, hour);
		console.log('before this.isOnline: ', this.isOnline);

		if (timeLogedIn < hour) {
			this.isOnline = true; // Correct assignment
		} else {
			this.isOnline = false; // Ensure isOnline is set to false otherwise
		}

		console.log('after this.isOnline: ', this.isOnline);
		return this.isOnline;
	};

	redirectTPongGame = () => {
		const currentHostname = window.location.hostname;
		const currentPort = window.location.port;

		const targetPort = currentPort !== '' ? currentPort : '8443'; // no port specified : use 8443
		const pongURL = `https://${currentHostname}:${targetPort}/pong/`;

		window.location.href = pongURL;
	};

	// NOTE: add method to fetch tournament winner and display it
	fetchTournamentWinner = (tournament_history) => {
		// fetch tournament winner
		const player1 = tournament_history.final_player1;
		const player2 = tournament_history.final_player2;

		const player1Score = tournament_history.final_score1;
		const player2Score = tournament_history.final_score2;

		//display tournament winner
		if (player1Score > player2Score) {
			return player1;
		} else {
			return player2;
		}
	};

	// NOTE: loop through tournament data to display all tournaments

	render() {
		return this._userTask.render({
			pending: () => html`<p>Loading dashboard...</p>`,
			complete: (user) => html`
				<div class="container container-fluid h-100">
					<section class="bg-light py-3 py-md-5 py-xl-8">
						<div class="container container-fluid w-100">
							<div class="row gy-4 gy-lg-0">
								<div class="col-12 col-lg-4 col-xl-3">
									<div class="row gy-4">
										<div class="col-12">
											<div class="card widget-card shadow-sm">
												<div class="card-header">
													<p>
														Hello, ${user.first_name}!
														<span>${this.checkIfOnline(user) ? 'Online' : 'Offline'}</span>
													</p>
												</div>

												<div class="card-body align-items-center">
													<div class="text-center mb-3">
														<img src=${this.link} class="img-fluid rounded-circle" alt="${user.login ? user.login : user.first_name}" />
													</div>
													<div class="card-body align-items-center">
														<h5 class="text-center mb-1">${user.displayname ? user.displayname : user.first_name + ' ' + user.last_name}</h5>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>

								<div class="col-12 col-lg-9 ">
									<div class="card widget-card shadow-sm">
										<div class="card-body container container-xxl">
											<div class="tab-content " id="profileTabContent">
												<div class="tab-pane fade show active" id="overview-tab-pane" role="tabpanel" aria-labelledby="overview-tab" tabindex="0">
													<h5 style="text-decoration: underline;" class="mb-3">Let's Play Pong!</h5>
													<button type="submit" class="btn btn-primary mt-3" href="/pong" @click="${this.redirectTPongGame}">Play Pong</button>
												</div>

												<h5 style="text-decoration: underline;" class="mb-3 pt-5">1v1 Dashboard</h5>
												<div class="container">
													<div class="row justify-content-center">
														<div class="card widget-card border-light shadow-sm">
															<div class="card-body p-4">
																<div class="table-responsive">
																	<table class="table table-borderless bsb-table-xl text-nowrap align-middle m-0">
																		<thead>
																			<tr>
																				<th>Date</th>
																				<th>Player 1</th>
																				<th>Score P1</th>
																				<th>Player 2</th>
																				<th>Score P2</th>
																				<th>Winner</th>
																				<th>Looser</th>
																			</tr>
																		</thead>
																		<tbody>
																			<tr>
																				<td><h6 class="mb-1">22/12/2021</h6></td>
																				<td><h6 class="mb-1">${user.first_name}</h6></td>
																				<td><h6 class="mb-1">12</h6></td>
																				<td><h6 class="mb-1">La Mere Noel</h6></td>
																				<td><h6 class="mb-1">777</h6></td>
																				<td><span class=" btn bg-success text-light">La Mere Noel</span></td>
																				<td><span class=" btn bg-danger text-light">${user.first_name}</span></td>
																			</tr>
																		</tbody>
																	</table>
																</div>
															</div>
														</div>
													</div>
													<br />

													<h5 style="text-decoration: underline;" class="mb-3 pt-5">Tournament Dashboard</h5>
													<div class="container">
														<div class="row justify-content-center">
															<div class="card widget-card border-light shadow-sm">
																<div class="card-body p-4">
																	<div class="table-responsive">
																		<table class="table table-borderless bsb-table-xl text-nowrap align-middle m-0">
																			<thead>
																				<tr>
																					<th>Date</th>
																					<th>Player 1</th>
																					<th>Score P1</th>
																					<th>Player 2</th>
																					<th>Score P2</th>
																					<th>Player 3</th>
																					<th>Score P3</th>
																					<th>Player 4</th>
																					<th>Score P4</th>
																					<th>Winner</th>
																				</tr>
																			</thead>
																			<tbody>
																				${this.tournamentData.tournament_history.map(
																					(tournament) => html`
																						<tr>
																							<td>
																								<h6 class="mb-1">
																									${new Date(tournament.final_start_time * 1000).toLocaleDateString()}
																								</h6>
																							</td>

																							<td><h6 class="mb-1">${user.first_name}</h6></td>
																							<td>
																								<h6 class="mb-1"></h6>
																								${tournament.semifinal1_score1}
																							</td>

																							<td><h6 class="mb-1">${tournament.semifinal1_player2}</h6></td>
																							<td>
																								<h6 class="mb-1"></h6>
																								${tournament.semifinal1_score2}
																							</td>

																							<td><h6 class="mb-1">${tournament.semifinal2_player1}</h6></td>
																							<td>
																								<h6 class="mb-1"></h6>
																								${tournament.semifinal2_score1}
																							</td>

																							<td><h6 class="mb-1">${tournament.semifinal2_player2}</h6></td>
																							<td>
																								<h6 class="mb-1"></h6>
																								${tournament.semifinal2_score2}
																							</td>
																							<td>
																								<span class=" btn bg-success text-light"
																									>${this.fetchTournamentWinner(tournament)}</span
																								>
																							</td>
																						</tr>
																					`
																				)}
																			</tbody>
																		</table>
																	</div>
																</div>
															</div>
														</div>
														<br />
														<h5 style="text-decoration: underline;" class="mb-2 pt-3">Profile</h5>
														<div class="card widget-card border-light shadow-sm">
															<div class="card-body p-4 widget-card row justify-content-center">
																<div class="tab-content pt-2" id="profileTabContent">
																	<div
																		class="tab-pane fade show active"
																		id="overview-tab-pane"
																		role="tabpanel"
																		aria-labelledby="overview-tab"
																		tabindex="0"
																	>
																		<div class="row g-0">
																			<div class="col-5 col-md-3 bg-light border-bottom border-white border-3">
																				<div class="p-2">First Name</div>
																			</div>
																			<div class="col-7 col-md-9 bg-light border-start border-bottom border-white border-3">
																				<div class="p-2">${user.first_name}</div>
																			</div>

																			<div class="col-5 col-md-3 bg-light border-bottom border-white border-3">
																				<div class="p-2">Last Name</div>
																			</div>
																			<div class="col-7 col-md-9 bg-light border-start border-bottom border-white border-3">
																				<div class="p-2">${user.last_name}</div>
																			</div>

																			<div class="col-5 col-md-3 bg-light border-bottom border-white border-3">
																				<div class="p-2">Username</div>
																			</div>
																			<div class="col-7 col-md-9 bg-light border-start border-bottom border-white border-3">
																				<div class="p-2">${user.login ? user.login : user.username}</div>
																			</div>

																			<div class="col-5 col-md-3 bg-light border-bottom border-white border-3">
																				<div class="p-2">Email</div>
																			</div>
																			<div class="col-7 col-md-9 bg-light border-start border-bottom border-white border-3">
																				<div class="p-2">${user.email}</div>
																			</div>
																			<div>
																				<a type="button" aria-current="page" class="nav-link btn btn-primary mt-3" href="/app/settingsPage">
																					Update Profile Info
																				</a>
																			</div>
																		</div>
																	</div>
																	<div
																		class="tab-pane fade"
																		id="profile-tab-pane"
																		role="tabpanel"
																		aria-labelledby="profile-tab"
																		tabindex="0"
																	></div>
																</div>
															</div>
														</div>
													</div>
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
customElements.define('dashboard-component', DashboardComponent);
