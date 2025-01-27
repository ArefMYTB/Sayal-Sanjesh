import { useEffect } from "react";
import mqtt from "mqtt";
import { toast } from "react-toastify";
// import { useSelector } from "react-redux";

const MQTT_BROKER = "ws://217.144.106.32:9999/mqtt";
const MQTT_USERNAME = "meters";
const MQTT_PASSWORD = "S@yal1402";
const MQTT_CHANNEL1 = "/Meters/TWM04";
const MQTT_CHANNEL2 = "/Meters/SWMM-02311201";
const MQTT_CHANNEL3 = "/Meters/SWMW-02411101";

const MqttClient = ({ projectId, update }) => {
  const namayesh = "bfce9060-83fa-4138-aec3-172b5df8291a";
  const test = "1f0dba9e-1ecd-48a0-b0b4-fa880f7985f1";
  const showEvent = (event, channel) => {
    //console.log(`event:${event} , channel : ${channel}`);
    if (channel === "1") {
      toast.info("کنتور فراصوت هوشمند (التراسونیک) آپدیت شد");
    }
    if (channel === "2") {
      toast.info("قرائت گر (مولتی جت) آپدیت شد");
    }
    if (channel === "3") {
      toast.info("ولتمن تست (ولتمن) آپدیت شد");
    }
    update();
    // const projects = useSelector((state) => state.projects);
    // const counters = useSelector((state) => state.counters);
    // const device = counters.filter(
    //   (counter) => counter.water_meter_serial === event.serial
    // );
    // if (projectId === event.project_id) {
    //   // toast.info(
    //   //   `آخرین مصرف برای کنتور ${device[0].water_meter_name} آپدیت شد`
    //   // );
    //   toast.info(
    //     <div>
    //       <div style={{ padding: "5px 0" }}>
    //         <strong>({event.event_type_code})</strong>-
    //         {event.event_type_keyword}
    //       </div>
    //       <div style={{ padding: "5px 0" }}>
    //         <strong>دستگاه:</strong> {event.meter_serial}
    //       </div>
    //       <div style={{ padding: "5px 0" }}>
    //         <strong>پروژه:</strong>{" "}
    //         {
    //           projects.filter(
    //             (project) => project.water_meter_project_id === event.project_id
    //           )[0].water_meter_project_name
    //         }
    //       </div>
    //     </div>
    //   );
    // }
  };
  useEffect(() => {
    const client = mqtt.connect(MQTT_BROKER, {
      username: MQTT_USERNAME,
      password: MQTT_PASSWORD,
    });
    client.on("connect", () => {
      //console.log("Connected to MQTT broker");
    });
    client.subscribe(MQTT_CHANNEL1);
    client.subscribe(MQTT_CHANNEL2);
    client.subscribe(MQTT_CHANNEL3);
    client.on("message", (topic, message) => {
      if (topic === MQTT_CHANNEL1) {
        projectId === namayesh || projectId === test
          ? showEvent(message.toString(), "1")
          : //console.log(message.toString());
      }
      if (topic === MQTT_CHANNEL2) {
        projectId === namayesh || projectId === test
          ? showEvent(message.toString(), "2")
          : //console.log(message.toString());
      }
      if (topic === MQTT_CHANNEL3) {
        projectId === namayesh || projectId === test
          ? showEvent(message.toString(), "3")
          : //console.log(message.toString());
      }
      // showEvent(message.toString());
      // //console.log(JSON.parse(message.toString()));
    });

    return () => {
      client.end();
    };
  }, []);

  return <></>;
};

export default MqttClient;
