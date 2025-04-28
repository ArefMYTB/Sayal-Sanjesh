import Card from "components/card";
import { MdAdd, MdDelete, MdEdit } from "react-icons/md";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import { OrderType } from "views/orders";
import { useState } from "react";
import OrderTypeForm from "components/forms/OrderTypeForm";

type OrderTypeTableData = Array<{
  orderTypeName: string;
  orderTypeCode: string;
  orderTypeCreateDate: string;
  orderTypeActions: JSX.Element;
}>;
const OrderTypesTable = () => {
  const [orderTypeName, setOrderTypeName] = useState<string>("");
  const {
    data: orderTypeData,
    isLoading: orderTypeIsLoading,
    status: orderTypeStatus,
    refetch: orderTypeRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("OrderType/admin/getAll", {
        page: 1,
        count: 10,
      }),
    queryKey: ["orderTypeList"],
  });

  const {
    isOpen: isOrderTypeOpen,
    onOpen: onOrderTypeOpen,
    onClose: onOrderTypeClose,
  } = useDisclosure();
  const editProjectClick = (id: string) => {
    // //console.log(id);
    // onOrderTypeOpen();
  };
  const renderTagActions = (adminId: string) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => {
            if (window.confirm("غیر فعال")) {
              editProjectClick(adminId)
            }
          }}
          icon={<MdEdit />}
          color="blue"
          extra="!p-2"
        />
      </div>
    );
  };
  const orderTypeTableHeader = [
    { title: "نام دستور", headerKey: "orderTypeName" },
    { title: "کد دستور", headerKey: "orderTypeCode" },
    { title: "تاریخ ایجاد", headerKey: "orderTypeCreateDate" },
    { title: "عملیات", headerKey: "orderTypeActions" },
  ];
  const tableData = () => {
    let orderTypesTableData: OrderTypeTableData = [];
    if (!orderTypeIsLoading && orderTypeStatus !== "pending") {
      orderTypeData.data.forEach((obj: OrderType) =>
        orderTypesTableData.push({
          orderTypeName: obj.order_type_name,
          orderTypeCode: obj.order_type_code,
          orderTypeCreateDate: toPersianDate(obj.order_type_create_time),
          orderTypeActions: renderTagActions(obj.order_type_id),
        })
      );
    }
    return orderTypesTableData;
  };
  return (
    <div className=" users-table-container">
      <CustomModal
        isOpen={isOrderTypeOpen}
        onClose={onOrderTypeClose}
        title={"نوع دستور"}
        modalType="form"
        information={null}
        modalForm={
          <OrderTypeForm
            orderTypeName={orderTypeName}
            setOrderTypeName={setOrderTypeName}
            onClose={onOrderTypeClose}
            updateTable={orderTypeRefetch}
          />
        }
      />
      <Card extra="border-none h-max">
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`انواع دستورات (${
              orderTypeIsLoading ? "loading..." : orderTypeData?.data.length
            })`}
          </div>
          <div className=" moldal-btns flex items-center justify-end">
            <CustomButton
              text="ایجاد دستور"
              onClick={onOrderTypeOpen}
              icon={<MdAdd />}
              color="green"
              extra="ml-4"
            />
          </div>
        </div>
        <SimpleTable
          header={orderTypeTableHeader}
          data={tableData()}
          hasIndex={true}
          extra="!h-[65vh]"
        />
      </Card>
      <div className="pagination my-4 py-4"></div>
    </div>
  );
};
export default OrderTypesTable;
