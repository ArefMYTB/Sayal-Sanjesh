// import {
//   TableContainer,
//   Table,
//   TableHead,
//   TableBody,
//   TableRow,
//   TableCell,
// } from "@material-ui/core";

import { useId } from "react";

// import { BLUE_COLOR, ERROR_COLOR, ORANGE_COLOR } from "../../utils/const";
interface BillCustomTableProps {
  header: string[];
  body: any[][];
  hcolspan: string;
  type: string;
  classes?: string;
}
// header = [name1,name2,...]
// body = [[a,b],[c,d]]
const BillCustomTable = ({
  header,
  body,
  hcolspan,
  type,
  classes,
}: BillCustomTableProps) => {
  const uniqId = useId();
  const typeColors = () => {
    if (type === "آب") {
      return "#0288d1";
    } else if (type === "برق") {
      return "#d32f2f";
    } else {
      return "#ed6c02";
    }
  };
  const headingStyle = {
    // color: "#ffffff",
    background: typeColors(),
  };
  return (
    <div className={classes} style={{ marginBottom: "10px" }}>
      <table
        className="!dark:border-white w-full"
        style={{ borderBottom: "1px solid #000" }}
      >
        <thead>
          <tr style={headingStyle}>
            {header.map((item, index) => (
              <th
                key={`${uniqId}_${index}`}
                colSpan={Number(hcolspan)}
                className=" border border-solid dark:!border-white"
                style={{
                  verticalAlign: "center",
                  border: "1px solid #000",
                  textAlign: "center",
                  padding: "0",
                }}
              >
                {item}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {body.map((item, idx) => (
            <tr key={`${uniqId}-${idx}`}>
              {item.map((d, i) => (
                <td
                  key={`${i}-${uniqId}-${idx}`}
                  className=" border border-solid dark:!border-white"
                  style={{
                    padding: " 0",
                    textAlign: "center",
                    minHeight: "20px",
                    border: "1px solid #000",
                  }}
                >
                  {d || d === 0 ? d : "__"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
export default BillCustomTable;
