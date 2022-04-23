import React, {Component} from 'react';
// import Cookies from 'universal-cookie';
import {useHistory,withRouter} from "react-router-dom";
import getWeb3 from "../getWeb3";
import SimpleStorageContract from "../contracts/SimpleStorage.json";
import NewsFeed from "../contracts/NewsFeed.json";
export const UserDataContext = React.createContext({
    storageValue: 0, web3: null, accounts: null, contract: null,newsFeed:null,news:null,pr:null
});

class UserDataContextProvider extends Component {
    state = { storageValue: 0, web3: null, accounts: null, contract: null ,newsFeed:null,news:null,pr:null};
    constructor(props) {
        super(props);
        this.addNewsToChain = this.addNewsToChain.bind(this);
        // this.setUserName = this.setUserName.bind(this);
        // this.updateToken = this.updateToken.bind(this);

    }

     async componentWillMount() {
         try {
             // Get network provider and web3 instance.
             const web3 = await getWeb3();

             // Use web3 to get the user's accounts.
             const accounts = await web3.eth.getAccounts();
             this.setState({accounts:accounts});
             // Get the contract instance.
             const networkId = await web3.eth.net.getId();
             this.setState({networkId:networkId});
             const deployedNetwork = NewsFeed.networks[networkId];
             const instance = new web3.eth.Contract(
                 NewsFeed.abi,
                 deployedNetwork && deployedNetwork.address,
             );
             this.setState({newsFeed: instance});
             this.setState({instance: instance});
             // const counter = await instance.methods.newsCount().call();
             // console.log(instance);
             // Set web3, accounts, and contract to the state, and then proceed with an
             // example of interacting with the contract's methods.
             // this.setState({web3, accounts, contract: instance}, this.runExample);
         } catch (error) {
             // Catch any errors for any of the above operations.
             alert(
                 `Failed to load web3, accounts, or contract. Check console for details.`,error
             );
             console.error(error);
         }
         // this.updateUserName();
         // console.log("fetched " + username);
         // this.setState({
         //     username:  fetchUserName(),
         // });
         this.setState({
             addNewsToChain: this.addNewsToChain,
         });
         // console.log("sadja");
         // const cookies = new Cookies();
         // let token=cookies.get('token');
         // console.log("using the token from cookie "+token);
         // console.log("accessing url"+urlMapper(USER_URL))
         // fetch(urlMapper(USER_URL) , {
         //     method: "GET",
         //     headers: {
         //         "Authorization":"Token "+token,
         //         "Accept": "application/json",
         //     },
         // }).then((response) => {
         //     if (response.ok) {
         //         return response.json();
         //     }
         //     console.log(this);
         //     this.props.history.push('/login');
         //     return {username: null,};
         // }).then((data) => {
         //     console.log("fetcting userName data=",data);
         //     // cookies.save()
         //     this.setState({
         //         username: data.username,
         //     });
         // });

     }

    async addNewsToChain(title,description) {
        console.log("request to add news to chain",title,description);
        console.log(this.state);
        await this.state.newsFeed.methods.addNews(title,description).send({from:this.state.accounts[0]});
        // let username = fetchUserName();
        // // let username = "sid";
        // this.setState({
        //     username: username,
        // });
    }
    // async updateToken(token) {
    //     this.setState({
    //         token: token,
    //     });
    // }
    //
    // async setUserName(username) {
    //     this.setState({
    //         username: username,
    //     });
    // }

    render() {
        return (
            <UserDataContext.Provider value={{...this.state}}>
                {this.props.children}
            </UserDataContext.Provider>
        );
    }
}

export default withRouter(UserDataContextProvider);