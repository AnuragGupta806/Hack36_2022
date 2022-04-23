// SPDX-License-Identifier: MIT
pragma solidity >=0.4.21 <8.10.0;
pragma experimental ABIEncoderV2;

contract NewsFeed
{
    uint256 constant reportThreshold=5; //if no. of reports reaches this, validtors will be assigned
    uint256 constant validatorCount=3; //no. of validators assigned to each news article for validation
    uint256 constant publishingCost=2; //cost to publish an article on the app

    uint256 public newsCount=0;
    enum State { Unverified, Fake, Verified }
    mapping(uint256=>News) public news_feed;
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
        payable(creator).transfer(msg.value);

        //assignValidators(newsCount);
    }

    function report(uint256 _index) payable public { //reader reports an article as fake news
        require(
            accContract.accountHasRole(msg.sender, uint(Accounts.Role.Reader))
        );
        if(news_feed[_index].news_state != State.Unverified) return;

        news_feed[_index].reporters.push(msg.sender);
        if(news_feed[_index].reporters.length >= reportThreshold) {
            assignValidators(_index);
        }
        readerStake[msg.sender][_index] = msg.value;
        payable(creator).transfer(msg.value);
    }

    function decideState(uint256 _index) private { //decides the state once all validators have voted
        if(news_feed[_index].upvotes > news_feed[_index].downvotes) {
            news_feed[_index].news_state = State.Verified;
        }
        else {
            news_feed[_index].news_state = State.Fake;
        }
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


    function addUpvote(uint256 _index) private { //validator votes as legitmiate news
        require(
            accContract.accountHasRole(msg.sender, uint(Accounts.Role.Validator))
        );
        news_feed[_index].upvotes_address.push(msg.sender);
        news_feed[_index].upvotes++;
    }

    function addDownvote(uint256 _index) private { //validator votes as fake news
        require(
            accContract.accountHasRole(msg.sender, uint(Accounts.Role.Validator))
        );
        news_feed[_index].downvotes_address.push(msg.sender);
        news_feed[_index].downvotes++;
    }

    function getNews(uint256 _index) public view returns(News memory){
        return news_feed[_index];
    }

    function getAllNews() public view returns (News[] memory){
        News[] memory all_news = new News[](newsCount);
        for(uint i=0;i<newsCount;i++){
            all_news[i] = news_feed[i];
        } 
        return all_news;
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

    function accountHasRole(address account, uint role) public view returns (bool) { //checks whether account has specified role
        return accountRoles[account][role];
    }
}
