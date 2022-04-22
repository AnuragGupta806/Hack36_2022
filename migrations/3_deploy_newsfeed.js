var NewsFeed = artifacts.require("./NewsFeed.sol");

module.exports = function(deployer) {
  deployer.deploy(NewsFeed);
};
