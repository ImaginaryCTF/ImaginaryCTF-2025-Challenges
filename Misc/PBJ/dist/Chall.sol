pragma solidity ^0.8.0;
contract PBJ {
    uint256 public flagCoin = 100;
    uint256 public eth; 
    uint256 public price; 
    uint256 public totalPrice;
    uint256 public k;
    uint256 public x;
    uint256 public y;
    uint256 public to_pay;
    uint256 public flag;
    mapping(address => uint256) public flags;
     constructor() payable {
         eth = msg.value; 
         k = eth * flagCoin;
     }
     function buy() payable public {
        flag = (msg.value*flagCoin)/(eth+msg.value);
        require(flag <= flagCoin,"Not enough flagCoin!");
        flagCoin =  flagCoin - flag;
        eth += msg.value;
        flags[msg.sender] += flag;
     }
     function sell(uint256 flag) payable public {
         require(flag <= flagCoin,"Not enough flagCoin!");
         require(flag <= flags[msg.sender],"You do not have that many flagCoins!");
         y = flag + flagCoin;
         x = k/y;
         to_pay = eth - x;
         flagCoin = y;
         eth = x;
         flags[msg.sender] -= flag;
         payable(msg.sender).transfer(to_pay);
     }
     function check_balance() public view returns (uint256) {
        return flags[msg.sender];
     }
     function priceForXFlagCoin(uint256 flag) public view returns (uint256) {
        return (k/(flagCoin-flag))-eth;
     }

     function isChallSolved() public view returns (bool) {
        return (msg.sender.balance / 1 ether) > 50;
    }
}