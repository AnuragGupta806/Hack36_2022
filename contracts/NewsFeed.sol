// SPDX-License-Identifier: MIT
pragma solidity >=0.4.21 <8.10.0;

contract NewsFeed
{
    uint256 constant reportThreshold=5; //if no. of reports reaches this, validtors will be assigned
    uint256 constant validatorCount=3; //no. of validators assigned to each news article for validation

    uint256 public newsCount=0;
    enum State { Unverified, Fake, Verified }
    enum Role { Reader, Validator, Publisher }
    mapping(uint256=>News) public news_feed;
    mapping(address => mapping(uint => bool)) accountRoles;
    address public creator;
    mapping(address => News) assignedArticle; //stores mapping of what articles is assigned to each validator at a given moment
    address[] freeValidators; //list of validators who have are idle
    address[] articleStake;
    mapping(address => mapping(uint => uint)) readerStake; //stores amount reader stakes on an article

    function accountAddRole(address account, Role role) internal { //adds specified role to account
        require(
            msg.sender == creator
        );
        accountRoles[account][uint(role)] = true;

        if(role == Role.Validator) {
            freeValidators.push(account);
        }
    }

    function accountHasRole(address account, Role role) internal
    view returns (bool) { //checks whether account has specified role
        return accountRoles[account][uint(role)];
    }

    struct News{
        uint256 id;
        address publisher;
        string title;
        string description;
        State news_state;
        uint256 upvotes;
        address[]  upvotes_address;
        uint256 downvotes;
        address[] downvotes_address;
        uint256 reportCount;
    }

    constructor() public { //called when contract is first created
        creator = msg.sender;
    }

    function addNews (string memory _title, string memory _description) payable public { //adds a news article
        require(
            accountHasRole(msg.sender, Role.Publisher)
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
            reportCount: 0
        });
       // payable(creator).transfer(msg.value);
    }

    function decideState(uint256 _index) private { //decides the state once all validators have voted
        if(news_feed[_index].upvotes > news_feed[_index].downvotes) {
            news_feed[_index].news_state = State.Verified;
        }
        else {
            news_feed[_index].news_state = State.Fake;
        }
    }


    function report(uint256 _index) payable public { //reader reports an article as fake news
        require(
            accountHasRole(msg.sender, Role.Reader)
        );
        if(news_feed[_index].news_state != State.Unverified) return;

        news_feed[_index].reportCount++;
        if(news_feed[_index].reportCount >= reportThreshold) {
            assignValidators(_index);
        }
        readerStake[msg.sender][_index] = msg.value;
       // payable(creator).transfer(msg.value);
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
            accountHasRole(msg.sender, Role.Validator)
        );
        news_feed[_index].upvotes_address.push(msg.sender);
        news_feed[_index].upvotes++;
    }

    function addDownvote(uint256 _index) private { //validator votes as fake news
        require(
            accountHasRole(msg.sender, Role.Validator)
        );
        news_feed[_index].downvotes_address.push(msg.sender);
        news_feed[_index].downvotes++;
    }
}
