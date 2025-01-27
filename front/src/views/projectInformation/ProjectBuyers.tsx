import SimpleTable, { HeaderObject } from "components/tables/SimpleTable";
import { DeviceObj } from "views/counters";
type BuyerTableData = {
  buyerName: string;
  buyerPhone: string;
  buyerDevices: string;
};
interface ProjectBuyersProps {
  projectDevices: DeviceObj[];
}
const ProjectBuyers = (props: ProjectBuyersProps) => {
  const { projectDevices } = props;
  let projectBuyersId: string[] = [];
  projectDevices.forEach((device: DeviceObj) => {
    if (
      device.water_meter_user__user_id &&
      !projectBuyersId.includes(device.water_meter_user__user_id)
    ) {
      projectBuyersId.push(device.water_meter_user__user_id);
    }
  });
  const tableData = () => {
    let buyersTableData: BuyerTableData[] = [];
    projectBuyersId.forEach((id: string) => {
      let userDevices: DeviceObj[] = projectDevices.filter(
        (device: DeviceObj) => device.water_meter_user__user_id === id
      );
      buyersTableData.push({
        buyerName: `${userDevices[0].water_meter_user__user_name} ${userDevices[0].water_meter_user__user_lastname}`,
        buyerPhone: `${userDevices[0].water_meter_user__user_phone}`,
        buyerDevices: `${userDevices.length} عدد`,
      });
    });
    return buyersTableData;
  };
  const tableHeaders: HeaderObject[] = [
    { title: "نام بهره بردار", headerKey: "buyerName" },
    { title: "شماره تماس", headerKey: "buyerPhone" },
    { title: "تعداد دستگاه", headerKey: "buyerDevices" },
  ];
  return (
    <>
      {projectBuyersId.length > 0 ? (
        <SimpleTable header={tableHeaders} data={tableData()} hasIndex={true} />
      ) : (
        <div>no buyer</div>
      )}
    </>
  );
};
export default ProjectBuyers;
