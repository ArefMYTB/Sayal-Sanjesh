import { useDisclosure } from "@chakra-ui/hooks";
import { useQuery } from "@tanstack/react-query";
import CustomButton from "components/button";
import Card from "components/card";
import { DynamicOption } from "components/fields/SelectInput";
import OrdersForm from "components/forms/OrdersForm";
import CustomModal from "components/modals";
import SimpleTable from "components/tables/SimpleTable";
import { useState } from "react";
import { MdSensors } from "react-icons/md";
import { reqFunction } from "utils/API";
import { renderTimeJalali } from "utils/TimeUtiles";

type OrderObject = {
  order_type: {
    order_type_id: string;
    order_type_code: string;
    order_type_name: string;
  };
  order_meter: {
    water_meter_serial: string;
    water_meter_name: string;
  };
  order_create_time: string;
  order_status_time: null | string;
  all_order_number: number;
  order_status: -1 | 0 | 1;
  order_id: string;
};
type Device = {
  water_meter_name: string;
  water_meter_serial: string;
  order_mode: null | "R" | "P";
};
export type OrderType = {
  order_type_id: string;
  order_type_code: string;
  order_type_name: string;
  order_type_create_time: Date;
  all_orders_number: number;
};
type OrderTableData = Array<{
  orderName: string;
  orderCode: string;
  orderDeviceName: string;
  orderDeviceSerial: string;
  orderSentTime: JSX.Element;
  orderReciveTime: JSX.Element;
  orderStatus: JSX.Element;
}>;
const OrdersView = () => {
  const [orderTypeSelect, setOrderTypeSelect] = useState<DynamicOption>(null);
  const [deviceSelect, setDeviceSelect] = useState<DynamicOption>(null);
  const {
    data: devicesData,
    isLoading: deviceIsLoading,
    status: deviceStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: 1,
        count: 100,
        user_id: null,
        project_id: null,
        water_meter_serial: null,
      }),
    queryKey: ["deviceList"],
  });
  const {
    data: orderType,
    isLoading: orderTypeIsLoading,
    status: orderTypeStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("OrderType/admin/getAll", {
        page: 1,
        count: 100,
      }),
    queryKey: ["orderTypeList"],
  });
  const {
    data: orderData,
    isLoading: orderIsLoading,
    status: orderStatus,
    refetch: ordersRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("Order/admin/getAll", {
        page: 1,
        count: 100,
        order_meter: null,
        order_type_id: null,
        order_type_code: null,
      }),
    queryKey: ["orderList"],
  });
  const {
    isOpen: isCreateOrderOpen,
    onOpen: onCreateOrderOpen,
    onClose: onCreateOrderClose,
  } = useDisclosure();
  const projectTableHeader = [
    { title: "نام دستور", headerKey: "orderName" },
    { title: "کد دستور", headerKey: "orderCode" },
    { title: "نام دستگاه", headerKey: "orderDeviceName" },
    { title: "سریال دستگاه", headerKey: "orderDeviceSerial" },
    { title: "زمان ارسال", headerKey: "orderSentTime" },
    { title: "زمان دریافت", headerKey: "orderReciveTime" },
    { title: "وضعیت دستور", headerKey: "orderStatus" },
  ];
  const tableData = () => {
    let projectTableData: OrderTableData = [];
    if (
      !orderIsLoading &&
      orderStatus !== "pending" &&
      !deviceIsLoading &&
      deviceStatus !== "pending"
    ) {
      orderData.data?.forEach((obj: OrderObject) =>
        projectTableData.push({
          orderName: obj.order_type.order_type_name,
          orderCode: obj.order_type.order_type_code,
          orderDeviceName: obj.order_meter.water_meter_name,
          orderDeviceSerial: obj.order_meter.water_meter_serial,
          orderSentTime: renderTimeJalali(obj.order_create_time, "chart"),
          orderReciveTime: renderTimeJalali(obj.order_status_time, "chart"),
          orderStatus: (
            <span
              className={`rounded ${
                obj.order_status === -1
                  ? "bg-red-600"
                  : obj.order_status === 0
                  ? "bg-yellow-600"
                  : " bg-green-600"
              } px-1 text-sm text-white`}
            >
              {obj.order_status === -1
                ? "دریافت نشده"
                : obj.order_status === 0
                ? "انجام نشده"
                : " انجام شده"}
            </span>
          ),
        })
      );
    }
    return projectTableData;
  };
  const renderDeviceSelectData = () => {
    let selectData: DynamicOption[] = [];
    if (!deviceIsLoading && deviceStatus === "success") {
      devicesData?.data?.forEach((device: Device) =>
        selectData.push({
          label: device.water_meter_name,
          value: device.water_meter_serial,
        })
      );
    }
    return selectData;
  };
  const renderOrderTypeSelectData = () => {
    let orderTypes: { label: string; value: string }[] = [];
    if (!orderTypeIsLoading && orderTypeStatus !== "pending") {
      orderType?.data?.forEach((type: OrderType) =>
        orderTypes.push({
          label: type.order_type_name,
          value: type.order_type_id,
        })
      );
    }
    return orderTypes;
  };
  return (
    <div className="">
      <CustomModal
        isOpen={isCreateOrderOpen}
        onClose={onCreateOrderClose}
        title={"ارسال دستور"}
        modalType="form"
        information={null}
        modalForm={
          <OrdersForm
            deviceSelectData={renderDeviceSelectData()}
            orderTypeSelectData={renderOrderTypeSelectData()}
            onClose={onCreateOrderClose}
            device={deviceSelect}
            setDevice={setDeviceSelect}
            orderType={orderTypeSelect}
            setOrderType={setOrderTypeSelect}
            updateTable={ordersRefetch}
          />
        }
      />
      <Card>
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`دستور ها (${
              orderIsLoading ? "loading..." : orderData?.data?.length ?? 0
            })`}
          </div>
          <div className=" moldal-btns flex items-center justify-end">
            <CustomButton
              text="ارسال دستور"
              onClick={onCreateOrderOpen}
              icon={<MdSensors />}
              color="green"
              extra="ml-4"
            />
          </div>
        </div>
        <SimpleTable
          header={projectTableHeader}
          data={tableData()}
          extra="h-[80vh]"
          // hasIndex={true}
        />
      </Card>
    </div>
  );
};
export default OrdersView;
