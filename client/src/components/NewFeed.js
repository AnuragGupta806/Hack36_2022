import React from "react";
import { useState,useEffect } from "react";
import Web3 from 'web3';
import NewsFeed from "../contracts/NewsFeed.json";

export default function NewFeed(){
    const [account, setAccount] = useState(); // state variable to set account.
    const [newsFeed,setNewsFeed]=useState();
    const [news,setNews]=useState([]);
    const [pr,setPr]=useState([]);

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
      // iterate through the amount of time of counter
      for (var i = 1; i <= counter; i++) {
        // call the contacts method to get that particular contact from smart contract
        const newt = await instance.methods.news_feed(i).call();
        // add recently fetched contact to state variable.
        setNews((news) => news.concat(newt));
      }
      }
      load();
     }, []);
     var showFeed='';
    for(var i=0;i<news.length;i++)
       showFeed+=`<li>${news[i]['title']}</li>`
    
     const addNews = async()=>{
        console.log("hello");
       await newsFeed.methods.addNews("testing","hello").send({from:account});
       var cr=await newsFeed.methods.newsCount().call();
       console.log(cr);
        // console.log(newsFeed.methods.newsCount().call());
    }
    return (
        <>
        <h1> News Feed</h1>
        <div>
            Your account is: {account}
        </div>
        {/* <ul>
      {
        Object.keys(news).map((newt, index) => (
            <h4>{newt['title']}</h4>
        ))
      }
      </ul> */}
        <ul dangerouslySetInnerHTML={{__html: showFeed}}></ul>
        <button onClick={addNews}>Add News</button>
        </>
    )
}