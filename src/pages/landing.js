import {React, Component } from "react";
import './landing.css'
import Candlestick from "./candles";

class LandingPage extends Component {
    render() {
      return (
        <div class="landing">
          <div>
          <div class="c-button"><button class="sign-in" ><span>Sign Up </span></button></div>
            <Candlestick/>
          </div>
        </div>
    )}
  }

export default LandingPage;