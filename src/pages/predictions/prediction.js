import React, { useEffect, useState } from "react";
import Navbar from "../navbar/nav";
import config from "../../config";
import "./prediction.css";

const Predictions = () => {

    const [pred, setPred] = useState([])
    const [query, setQuery] = useState("")
    const today = new Date()
    const tomorrow = new Date(today);

    tomorrow.setDate(tomorrow.getDate() + 1)

    const configDate = {
      year: "numeric",
      month: "long",
      day: "2-digit"
    }

    const DTF = new Intl.DateTimeFormat('default', configDate);
    const d = DTF.format(tomorrow)

    useEffect(() => {
        fetch(`${config.baseUrl}/predictions/get_predictions`, {
          method: "GET"
        })
          .then((res) => res.json())
          .then(({ error, data }) => {
            setPred(data)
          })
      }, []);

    return(
      <div className="pred-main">
      <Navbar />
        <div className="predictions-wrapper">
            <h1 className="p-heading"> Predictions for {d}</h1>
            <input type="text" placeholder="Enter Ticker..."  className="pred-search" onChange={(e) => setQuery(e.target.value)}/>
            <ul className="pred-list">
              {pred.filter(stock => stock["Ticker"].toLowerCase().includes(query.toLowerCase())).map( (val) => (
                <>
                  <div className="pred-items">
                    <li key={val.ticker}>
                      <div className="pitem-ticker">{val["Ticker"]}</div>
                      <div className="pitem-price">Predicted Price: {val["Price"]}</div>
                    </li>
                  </div>
                </>
              ))}
            </ul>
        </div>
        </div>
    )
}

export default Predictions;