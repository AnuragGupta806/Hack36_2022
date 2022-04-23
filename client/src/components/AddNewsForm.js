import React, {useContext, useState} from "react";
import {Button, FormControl, FormHelperText, Input, InputLabel} from "@mui/material";
import {UserDataContext} from "../contexts/UserDataContext";
const  AddNewsForm=(data)=>{

    // const addNewsToChain=data.addNewsToChain;
    // const qq=useContext(UserDataContext);
    const {addNewsToChain}=useContext(UserDataContext);
    console.log("addNewsToChain",addNewsToChain);
    // console.log("qq",qq);
    const [title,setTitle]=useState();
    const [desc,setDesc]=useState();
    const onTitleChange=(e)=>{
        e.preventDefault();
        setTitle(e.target.value);
    }
    const onDescChange=(e)=>{
        e.preventDefault();
        setDesc(e.target.value);
    }
    return (

        <div>
            <div>
                <InputLabel htmlFor="my-title">Title</InputLabel>
                <Input onChange={onTitleChange} id="my-title" aria-describedby="my-title-helper-text" />
                <FormHelperText id="my-title-helper-text">We'll never share your email.</FormHelperText>
            </div>
            <div>
                {/*<InputLabel htmlFor="my-description">Description</InputLabel>*/}
                <Input onChange={onDescChange} id="my-description" aria-describedby="my-description-helper-text" />
                {/*<FormHelperText id="my-description-helper-text">We'll never share your email.</FormHelperText>*/}
            </div>
            <Button onClick={()=>{
                addNewsToChain(title,desc);
            }}>Submit</Button>
        </div>


    );
}
export default AddNewsForm;