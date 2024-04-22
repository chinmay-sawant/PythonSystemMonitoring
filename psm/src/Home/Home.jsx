import { useEffect, useState } from "react";
import { CPURAM } from "../health/CPURAM";
import PieChart from "../health/PieChart";
import "./Home.css";
import RadarChart from "../health/RadarChart";
export const Home = () => {
  const [eventData, setEventData] = useState({});
  const [diskUsuageData, setDiskUsageData] = useState({});
  const [ramUsageData, setRamUsageData] = useState({});
  const [radarGraphData, setRadarGraphData] = useState({});
  const [hostname,setHostname] = useState("Default HostName");
  const [ipaddress,setIpaddress] = useState("0.0.0.0");
  const [macAddress,setMacAddress] = useState("00:00:00:00:00:00");
  const [timeStamp,setTimeStamp] = useState(null);

  const updateEventData = (data) => {
    setEventData(data);
     console.log("data updated !!",data)
  };

  useEffect(() => {
    if (Object.keys(eventData).length === 0) {
      // eventData is empty, don't do anything
    } else {
      setHostname(eventData["hostname"])
      setIpaddress(eventData["ipaddress"])
      setMacAddress(eventData["macaddress"])
      setTimeStamp(eventData["timestamp"])
      var diskData = eventData["health"]["disk"];
      var DiskUsageLabels = [];
      var DiskUsageValues = [];
      var RamUsageLabels = [];
      var RamUsageValues = [];

      for (const key in diskData) {
        if (diskData.hasOwnProperty(key)) {
          const device = diskData[key]["device"];
          const percent = diskData[key]["percent"];
          DiskUsageLabels.push(device)
          DiskUsageValues.push(percent)
         //  console.log(`Key: ${key}, Device: ${device}`);
        }
      }

      const diskUsuageData = {
        labels: DiskUsageLabels,
        values: DiskUsageValues,
      };

      const ramUsageData = {
        labels: ["Used","Free"],
        values: [eventData["health"]["ram"]["percent"],parseFloat(100-eventData["health"]["ram"]["percent"])],
      };    
      let alldiskvalues = DiskUsageValues.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

      const radarGraphData = {
        labels: ["RAM","CPU","Storage"],
        values1: [eventData["health"]["ram"]["percent"],eventData["health"]["cpu"]["percent"],alldiskvalues/DiskUsageValues.length],
        values2: [100-eventData["health"]["ram"]["percent"],100-eventData["health"]["cpu"]["percent"],100-(alldiskvalues/DiskUsageValues.length)]
      };

      setDiskUsageData(diskUsuageData);
      setRamUsageData(ramUsageData);
      setRadarGraphData(radarGraphData);
    }
  }, [eventData]);

  return (
    <>
    <div className="accordion accordion-flush" id="accordionFlushExample">
  <div className="accordion-item">
    <h2 className="accordion-header">
      <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
      <h3>
      <span>Hostname - {hostname}</span>
      </h3>
 
      </button>
    </h2>
    <div id="flush-collapseOne" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
      <div className="accordion-body">
      <h3>
          <span>Hostname - {hostname}</span>
          <ul>
          <li>
            Ipaddress - {ipaddress}
          </li>  
          <li>
            Mac Address - {macAddress}
          </li>  
          <li>
            TimeStamp - {timeStamp}
          </li>  
          </ul>
          
        </h3>
        <br/>

      </div>
    </div>
  </div>
  </div>
      <div className="container">
        
        <div className="row row-cols-1 row-cols-md-2 g-4">
          <div className="col">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">CPU and RAM</h5>
                <CPURAM updateEventData={updateEventData} />
              </div>
            </div>
          </div>
          <div className="col">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">Disk Usage</h5>
                <PieChart data={diskUsuageData} />
              </div>
            </div>
          </div>
        </div>
        <hr></hr>
        <div className="row row-cols-1 row-cols-md-2 g-4">
        <div className="col">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">Ram Usage</h5>
                <PieChart data={ramUsageData} />
              </div>
            </div>
          </div>
          <div className="col">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">System Performance</h5>
                <RadarChart data2={radarGraphData} />
              </div>
            </div>
          </div>
        </div>
      </div>
      
    </>
  );
};
