import React,{useState, useEffect} from 'react'
import "../styles/settings.css";
import { BrowserRouter as  useParams, Link} from "react-router-dom";


function Plant_Settings () {
  const [user] = useState(sessionStorage.getItem('User'));
  const [systemID] = useState(sessionStorage.getItem('SysID'));
  const [pumpOnTime, setPOT] = useState()
  const [moistureCutoff, setMCO] = useState()
  const [delay, setDelay] = useState()
  const [activePump, setAP] = useState()
  const [num] = useState()

  const POThandler = (event) => {setPOT(event.target.value);}
  const MCOhandler = (event) => {setMCO(event.target.value);}
  const Delayhandler = (event) => {setDelay(event.target.value);}
  const APhandler = (event) => {setAP(event.target.value);}


  // const remove = async () => {}

  const probeSet = async () => {
    const response = await fetch("https://myapws-e951a7210fa4.herokuapp.com/update_settings", {
        method: 'POST',
        mode: "cors",
        headers:{
            'content-Type':'application/json'
        },
        body: JSON.stringify({
          username: user,
          systemID: systemID,
          settings: [pumpOnTime, moistureCutoff, delay, activePump]
        })
    })
    const data = await response.json();
    alert(data['message'])
    sessionStorage.removeItem('SysID');
    window.location.replace('/Dashboard')
  }

  return (
    <div id = "settingsback">
        <div id = "plantSettings">
          <h1 id = "settingtext2">System Settings</h1>
            <br />
            <div class="horizontal-container">
              <label id = "settingtext" >Pump On Time </label>
              <input type='POT' value={num} onChange={POThandler} required id='settings' pattern="[0-9]+" ></input>
              <label>seconds</label>
            </div>

            <br/><br/>

            <div class="horizontal-container">
              <label id = "settingtextMT">Moisture Threshold    </label>
              <input type='MCO' value={num} onChange={MCOhandler} required id='settingsMT' pattern="[0-9]+" ></input>
              <label>level</label>
            </div>

            <br/><br/>

            <div class="horizontal-container">
              <label id = "settingtext">Reading Frequency   </label>
              <input type='DT' value={num} onChange={Delayhandler} required id='settings' pattern="[0-9]+" ></input>
              <label>minutes</label>
            </div>

            <br/><br/>

            <div class="horizontal-container">
              <label id = "settingtext">Pump Active Time   </label>
              <input type='AP' value={num} onChange={APhandler} required id='settings' pattern="[0-9]+" ></input>
              <label>seconds</label>
            </div>

            <br/><br/>
            <button onClick={probeSet} id='FPBtn'>Update Settings</button> 
            <br/><br/>
            <Link to='/Dashboard' id = "Sbacklink">Back To Dashboard</Link> <br />
        </div>
    </div>
    );
}

export default Plant_Settings