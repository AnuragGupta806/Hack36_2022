// SPDX-License-Identifier: MIT
pragma solidity >=0.4.21 <8.10.0;
pragma abicoder v2;

contract NewsFeed
{
    uint256 constant reportThreshold=5; //if no. of reports reaches this, validtors will be assigned
    uint256 constant validatorCount=3; //no. of validators assigned to each news article for validation
    uint256 constant publishingCost = 500000000000000000 wei; //0.5 ether, cost to publish an article on the app
    uint256 constant readingCost = 10000000000000000 wei; //0.01 ether, cost to read an article
    uint256 constant reportStake = 100000000000000000 wei; //0.1 ether, amount reader stakes to report an article

    uint256 public newsCount=0;
    enum State { Unverified, Fake, Verified }
    mapping(uint256=>News) news_feed;
    string[] articleTitles; //stores only titles, for showing feed
    address public creator;
    mapping(address => News) assignedArticle; //stores mapping of what articles is assigned to each validator at a given moment
    address[] freeValidators; //list of validators who are idle
    address[] articleStake;
    mapping(address => mapping(uint => uint)) readerStake; //stores amount reader stakes on an article
    Accounts accContract;


    struct News {
        uint256 id;
        address publisher;
        string title;
        string description;
        State news_state;
        uint256 upvotes;
        address[]  upvotes_address;
        uint256 downvotes;
        address[] downvotes_address;
        address[] reporters;
    }

    constructor(Accounts _accContract) public { //called when contract is first created
        creator = msg.sender;
        accContract = _accContract;
    }

    function addNews (string memory _title, string memory _description) payable public { //adds a news article
        require(
            accContract.accountHasRole(msg.sender, uint(Accounts.Role.Publisher))
        );
        require(
            msg.value >= publishingCost
        );
        newsCount++;
        news_feed[newsCount]=News({
            id: newsCount,
            publisher: msg.sender,
            title: _title,
            news_state: State.Unverified,
            description: _description,
            upvotes: 0,
            downvotes: 0,
            upvotes_address: new address [](0),
            downvotes_address: new address [](0),
            reporters: new address [](0)
        });
        articleTitles.push(_title);
        //payable(creator).transfer(msg.value);
    }

    function getFeed() public returns (string[] memory) {
        return articleTitles;
    }

    function readNews(uint256 _index) public payable returns (News memory) {
        require(
            accContract.accountHasRole(msg.sender, uint(Accounts.Role.Reader))
        );
        require(
            msg.value >= readingCost
        );
        return news_feed[_index];
    }

    function report(uint256 _index) payable public { //reader reports an article as fake news
        require(
            accContract.accountHasRole(msg.sender, uint(Accounts.Role.Reader))
        );
        if(news_feed[_index].news_state != State.Unverified) return;

        news_feed[_index].reporters.push(msg.sender);
        if(news_feed[_index].reporters.length >= reportThreshold) {
            assignValidators(_index); //assuming for now there are always enough validators
        }
        readerStake[msg.sender][_index] = msg.value;
    }


    function assignValidators(uint256 _index) private { //contract assigns validators when enough readers have reported
        uint cnt = validatorCount;
        while(cnt > 0) {
            address currentValidator = freeValidators[freeValidators.length - 1];
            freeValidators.pop();
            assignedArticle[currentValidator] = news_feed[_index];
            cnt--;
        }
    }


    function addUpvote(uint256 _index) public { //validator votes as legitmiate news
        require(
            accContract.accountHasRole(msg.sender, uint(Accounts.Role.Validator))
        );
        news_feed[_index].upvotes_address.push(msg.sender);
        news_feed[_index].upvotes++;

        delete assignedArticle[msg.sender];
        freeValidators.push(msg.sender);

        if(news_feed[_index].upvotes + news_feed[_index].downvotes == validatorCount) { decideState(_index); }
    }

    function addDownvote(uint256 _index) public { //validator votes as fake news
        require(
            accContract.accountHasRole(msg.sender, uint(Accounts.Role.Validator))
        );
        news_feed[_index].downvotes_address.push(msg.sender);
        news_feed[_index].downvotes++;

        delete assignedArticle[msg.sender];
        freeValidators.push(msg.sender);

        if(news_feed[_index].upvotes + news_feed[_index].downvotes == validatorCount) { decideState(_index); }
    }

    function decideState(uint256 _index) private { //decides the state once all validators have voted
        if(news_feed[_index].upvotes > news_feed[_index].downvotes) {
            news_feed[_index].news_state = State.Verified;

            uint totalStake = news_feed[_index].reporters.length * reportStake;
            payable(news_feed[_index].publisher).transfer(totalStake);
        }
        else {
            news_feed[_index].news_state = State.Fake;

            uint amtToEachReporter = publishingCost / reportThreshold;
            for(uint i = 0; i < news_feed[_index].reporters.length; i++) {
                payable(news_feed[_index].reporters[i]).transfer(amtToEachReporter);
            }
        }
    }
}


contract Accounts {
    address public creator;
    mapping(address => mapping(uint => bool)) accountRoles;
    enum Role { Reader, Validator, Publisher }
    address[] freeValidators;

    constructor() public {
        creator = msg.sender;
    }

    function accountAddRole(address account, uint role) public { //adds specified role to account
        require(
            msg.sender == creator
        );
        accountRoles[account][role] = true;

        if(role == uint(Role.Validator)) {
            freeValidators.push(account);
        }
    }

    function accountHasRole(address account, uint role) public returns (bool) { //checks whether account has specified role
        return accountRoles[account][role];
    }
}
