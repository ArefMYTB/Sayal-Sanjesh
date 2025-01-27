import CustomButton from "components/button";
import BillBody from "./BillBody";
import BillFooter from "./BillFooter";
import BillHeader from "./BillHeader";
import { BillObject } from "./ShowBills";
import JsPDF from "jspdf";
import html2canvas from "html2canvas";
// import html2PDF from "jspdf-html2canvas";
import "../../assets/css/new.css";

interface BillComponentProps {
  billInfo: BillObject;
  onClose?: Function;
  patternSample: { k: string; v1: string; v2: string }[];
}
const BillComponent = (props: BillComponentProps) => {
  const { billInfo, onClose, patternSample } = props;
  let billType =
    billInfo?.bill_water_meter.water_meter_type_info.water_meter_tag_info
      .water_meter_tag_name;

  const downloadBill = () => {
    const options = {
      scrollY: -window.scrollY,
      windowWidth:
        document.documentElement.offsetWidth * window.devicePixelRatio,
      windowHeight:
        document.documentElement.offsetHeight * window.devicePixelRatio,
      useCORS: true,
    };
    const input = document.getElementById("report");
    html2canvas(input, options).then((canvas) => {
      const imgData = canvas.toDataURL("image/png");
      const pdf = new JsPDF({
        orientation: "landscape",
        unit: "mm",
        format: [215, 150], // A5 paper size in landscape
      });
      pdf.addImage(imgData, "PNG", 0, 0, 215, 150); // Add the image to PDF
      pdf.save(`bill_${billInfo?.bill_water_meter?.water_meter_name}.pdf`);
    });
  };
  return (
    <>
      <div className=" overflow-x-scroll">
        <div
          className="bill-info"
          id="report"
          style={{
            width: "215mm",
            height: "150mm",
            margin: "10px auto",
          }}
        >
          <BillHeader info={billInfo} />
          <BillBody info={billInfo} type={billType} />
          <BillFooter
            info={billInfo}
            type={billType}
            patternSample={patternSample}
          />
        </div>
      </div>
      <div className="flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => downloadBill()}
          text={`دانلود`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </>
  );
};
export default BillComponent;
