import React, {useContext} from "react";
import {useState, useEffect} from "react";
import Web3 from 'web3';
import NewsFeed from "../contracts/NewsFeed.json";
import * as PropTypes from "prop-types";
import AddNewsForm from "./AddNewsForm";
import NewsFeedCard from "./NewsFeedCard";
import {UserDataContext} from "../contexts/UserDataContext";

// const NewsFeedCard = ()=>{
//    return(
//        <div className="">
//             <Card className=""/>
//        </div>
//    );
// };

// NewsFeedCard.propTypes = {
//     description: PropTypes.any,
//     title: PropTypes.any
// };
export default function NewFeed() {
    const [account, setAccount] = useState(); // state variable to set account.
    const [newsFeed, setNewsFeed] = useState();
    const [news, setNews] = useState([]);
    const [pr, setPr] = useState([]);
    // const {instance} = useContext(UserDataContext);
    const [showFeed,setShowFeed] = useState([]);
    let sf = [];
    useEffect(() => {
        async function load() {
                const web3 = new Web3(Web3.givenProvider || 'http://localhost:7545');
                const accounts = await web3.eth.requestAccounts();
                setAccount(accounts[0]);
                const networkId = await web3.eth.net.getId();
                 const deployedNetwork = NewsFeed.networks[networkId];
                 const instance = new web3.eth.Contract(
                NewsFeed.abi,
                deployedNetwork && deployedNetwork.address,
              );
              setNewsFeed(instance);
            const counter = await instance.methods.newsCount().call();
            //   console.log(counter);
            //   // iterate through the amount of time of counter
            for (var i = 1; i <= counter; i++) {
                //     // call the contacts method to get that particular contact from smart contract
                const newt = await instance.methods.news_feed(i).call();
                // await instance.methods.addNews("test11", "ttfdg");
                //     // add recently fetched contact to state variable.
                setNews((news) => news.concat(newt));
            }
        }
        load();

        // setNewsFeed(sf);
    }, []);

    console.log("newssdfsd", news);
    for (var i = 0; i < news.length; i++) {
        let title = news[i]['title'];
        let description = news[i]['description'];
        let id = news[i][0];
        console.log("id",id);
        let qq=[title,description];
        // sf.push(<h1>{title}</h1>);
        sf.push(<NewsFeedCard key={i} data={{title:title,description:description}}/>);
        console.log("title is",title);
        // description = {news[i]['description']}
        // sf.push(<NewsFeedCard data={{title: news[i]['title'], description: news[i]['description']}}/>);
    }


    // console.log("s",sf);
    return (
        <div>
            <h1> News Feed</h1>
            <div>
                Your account is: {account}
            </div>
            {sf.map(feed=>{
                return feed;
            })}
            <AddNewsForm/>
        </div>
    );
}

