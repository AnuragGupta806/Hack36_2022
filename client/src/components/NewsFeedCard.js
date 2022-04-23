import React from "react";

const NewsFeedCard=({data})=>{
    const {title, description}=data;
    console.log(title);
    // console.log(data.description);
    return (
        <div >
            <h1>
                News :
                {title} {description}
            </h1>
        </div>
    );
};
export default NewsFeedCard;