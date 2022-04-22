import React from "react";
import { useState,useEffect } from "react";
import Web3 from 'web3';
export default function NewFeed(){
    const [account, setAccount] = useState(); // state variable to set account.
    const [newsFeed,setNewsFeed]=useState([]);
    useEffect(() => {
      async function load() {
        const web3 = new Web3(Web3.givenProvider || 'http://localhost:7545');
        const accounts = await web3.eth.requestAccounts();
        
        setAccount(accounts[0]);
      }
      
      load();
     }, []);
    return (
        <>
        <h1> News Feed</h1>
        <div>
            Your account is: {account}
        </div>
        </>
    )
}