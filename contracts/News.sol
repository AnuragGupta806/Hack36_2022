// SPDX-License-Identifier: MIT
pragma solidity >=0.4.21 <8.10.0;

contract NewsFeeds
{
    uint256 public newsCount=0;
    enum State { Unverified, Fake, Verified }
    mapping(uint256=>News) public news_feed;
    struct News{
        uint256 id;
        address publisher;
        string title;
        string description;
        State news_state;
    }
    function addNews(string memory _publisher,string memory _description) public{
        newsCount++;
        news_feed[newsCount]=News(newsCount,msg.sender,_publisher,_description,State.Unverified);
        changeStateVerify(newsCount);
    }
    function changeStateVerify(uint256 _index) private{
        news_feed[_index].news_state=State.Verified;
    }
    function changeStateFake(uint256 _index) private{
        news_feed[_index].news_state=State.Fake;
    }
}