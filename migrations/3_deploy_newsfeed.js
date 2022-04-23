var NewsFeed = artifacts.require("NewsFeed");
var Accounts = artifacts.require("Accounts");
// module.exports = function(deployer) {
//   deployer.deploy(NewsFeed);
// };

module.exports = function(deployer) {
  deployer.deploy(Accounts).then(function(){
        return deployer.deploy(NewsFeed, Accounts.address)
});
};