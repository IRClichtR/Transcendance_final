// SPDX-License-Identifier: MIT
pragma solidity >=0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract pongData is Ownable {
	
	struct pongGame {
		uint256 semifinal1_start_time;
		uint256 semifinal2_start_time;
		uint256 final_start_time;
		string semifinal1_player1;
		string semifinal1_player2;
		string semifinal2_player1;
		string semifinal2_player2;
		string final_player1;
		string final_player2;
		uint8 semifinal1_score1;
		uint8 semifinal1_score2;
		uint8 semifinal2_score1;
		uint8 semifinal2_score2;
		uint8 final_score1;
		uint8 final_score2;
	}	

	pongGame[] public pongGames;

	constructor() Ownable(msg.sender) {}
	//new game has been played
	function storeGame(
		uint256 _semifinal1_start_time,
        string memory _semifinal1_player1,
        string memory _semifinal1_player2,
        uint8 _semifinal1_score1,
        uint8 _semifinal1_score2,
        uint256 _semifinal2_start_time,
        string memory _semifinal2_player1,
        string memory _semifinal2_player2,
        uint8 _semifinal2_score1,
        uint8 _semifinal2_score2,
        uint256 _final_start_time,
        string memory _final_player1,
        string memory _final_player2,
        uint8 _final_score1,
        uint8 _final_score2
	) external onlyOwner {
		pongGames.push(pongGame(
			_semifinal1_start_time,
            _semifinal2_start_time,
            _final_start_time,
            _semifinal1_player1,
            _semifinal1_player2,
            _semifinal2_player1,
            _semifinal2_player2,
            _final_player1,
            _final_player2,
            _semifinal1_score1,
            _semifinal1_score2,
            _semifinal2_score1,
            _semifinal2_score2,
            _final_score1,
            _final_score2
		));
	}

	function getPongGames() external view returns(pongGame[] memory) {
		return pongGames;
	}
}	
