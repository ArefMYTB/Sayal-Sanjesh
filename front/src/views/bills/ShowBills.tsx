import { ProjectObject } from "views/projects";
import BillSelectFilter from "./BillSelectFilter";
import { DeviceObj, TagObject } from "views/counters";
import { DynamicOption } from "components/fields/SelectInput";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import { MdRemoveRedEye } from "react-icons/md";
import CustomButton from "components/button";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import BillComponent from "./BillComponent";
import moment from "moment";
import Loading from "components/loading";
import { renderUnit } from "utils/CommonFunctions";
import { renderToast } from "utils/globalUtils";
interface ShowBillsProps {
  projects: ProjectObject[];
  tags: TagObject[];
}
type BillTableData = {
  billSerial: string;
  billFrom: string;
  billTill: string;
  startBillNumber: string;
  endBillNumber: string;
  consumptions: string;
  averageConsumption: string;
  price: string;
  deadLine: string;
  billActions: JSX.Element;
};
export type BillObject = {
  bill_id: string;
  bill_serial: string;
  bill_start_date: Date;
  bill_end_date: Date;
  payment_dead_line: Date;
  bill_create_date: Date;
  consumptions: number;
  bill_price: number;
  other_information: {
    bill_factor?: number;
    pay_details?: string;
    period_days?: number;
    price_words?: string;
    bill_details?: string;
    end_period_sum?: number;
    start_period_sum?: number;
  };
  bill_water_meter: {
    water_meter_serial: string;
    water_meter_name: string;
    water_meter_activation: number;
    water_meter_validation: number;
    water_meter_condition: number;
    water_meter_location:
      | string
      | { lat: string | number; lng: string | number };
    water_meter_create_date: Date;
    other_information: {
      test?: string;
      bill_factor?: number;
      description?: string;
    };
    water_meter_project_info: {
      water_meter_project_id: string;
      water_meter_project_name: string;
      water_meter_project_title: string;
      water_meter_project_files: [];
      water_meter_project_start_date: Date;
      water_meter_project_employer_description: {
        name: string;
        lastName: string;
        phoneNumber: string;
      };
      water_meter_project_contract_number: string;
      water_meter_project_images: [];
      water_meter_project_urls: {
        logo: string;
        gallery: string[];
      };
    };
    water_meter_type_info: {
      water_meter_type_id?: string;
      water_meter_type_name?: string;
      water_meter_tag_info?: {
        water_meter_tag_name?: string;
        water_meter_tag_id?: string;
      };
    };
    water_meter_module_info?: {
      water_meter_module_id?: string;
      water_meter_module_code?: string;
      water_meter_module_name?: string;
    };
  };
  bill_link: null | string;
  bill_link_validation: boolean | null;
  all_bill_count: number;
};
const ShowBillView = (props: ShowBillsProps) => {
  const { projects, tags } = props;
  const [project, setProject] = useState<DynamicOption>(null);
  const [tag, setTag] = useState<DynamicOption>(null);
  const [counter, setCounter] = useState<DynamicOption>(null);
  const [billInfo, setBillInfo] = useState<BillObject>(null);
  const {
    data: projectDeviceData,
    isLoading: projectDeviceIsLoading,
    status: projectDeviceStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: 1,
        count: 100,
        user_id: null,
        project_id: project ? project.value : null,
        water_meter_serial: null,
      }),
    queryKey: ["projectDevice", project],
  });
  const {
    data: billsData,
    isLoading: billsIsLoading,
    status: billsStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("bills/admin/getAll", {
        page: 1,
        count: 30,
        water_meter_serial: counter.value,
        bill_serial: null,
        bill_start_date: null,
        user_id: null,
        user_phone_number: null,
        project_id: null,
        bill_end_date: null,
        payment_dead_line: null,
        bill_create_date: null,
      }),
    queryKey: ["projectDevice", counter],
  });
  if (billsData?.code === 200) {
  } else {
    renderToast(
      billsData?.farsi_message
        ? billsData.farsi_message
        : "در مشاهده قبوض خطایی رخ داده",
      "err"
    );
  }
  const {
    data: patternData,
    isLoading: patternIsLoading,
    status: patternStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("Pattern/admin/getAll", {
        page: 1,
        count: 10,
        project_id: project ? project.value : null,
        tag_id: tag ? tag.value : null,
      }),
    queryKey: ["billsPatternList", tag, project],
  });
  const {
    isOpen: isBillOpen,
    onOpen: onBillOpen,
    onClose: onBillClose,
  } = useDisclosure();
  const showBillClick = (billInfo: BillObject) => {
    setBillInfo(billInfo);
    onBillOpen();
  };
  const renderBillActions = (billInfo: BillObject) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => showBillClick(billInfo)}
          icon={<MdRemoveRedEye />}
          color="blue"
          extra="!p-2"
        />
      </div>
    );
  };
  const renderProjectSelectData = () => {
    let selectData: DynamicOption[] = [];
    projects?.length > 0
      ? projects.forEach((project) =>
          selectData.push({
            label: project.water_meter_project_name,
            value: project.water_meter_project_id,
          })
        )
      : (selectData = []);
    return selectData;
  };
  const renderTagSelectData = () => {
    let selectData: DynamicOption[] = [];
    tags.length > 0
      ? tags.forEach((tag) =>
          selectData.push({
            label: tag.water_meter_tag_name,
            value: tag.water_meter_tag_id,
          })
        )
      : (selectData = []);
    return selectData;
  };
  const renderCounterSelectData = () => {
    let selectData: DynamicOption[] = [];
    if (!projectDeviceIsLoading && projectDeviceStatus === "success" && tag) {
      let filteredCounter = projectDeviceData?.data?.filter(
        (device: DeviceObj) =>
          device.water_meter_type__water_meter_tag__water_meter_tag_id ===
          tag.value
      );
      filteredCounter?.length > 0
        ? filteredCounter?.forEach((counter: DeviceObj) => {
            selectData.push({
              label: counter.water_meter_name,
              value: counter.water_meter_serial,
            });
          })
        : (selectData = []);
    }
    return selectData;
  };
  const counterInfoTableHeader = [
    { title: "نام کنتور", headerKey: "counterName" },
    { title: "شماره سریال", headerKey: "counterSerial" },
    // { title: "دسته کنتور", headerKey: "counterTag" },
    { title: "نوع کنتور", headerKey: "counterType" },
    { title: "مالک کنتور", headerKey: "owner" },
  ];
  const billsTableHeader = [
    { title: "شناسه قبض", headerKey: "billSerial" },
    { title: "شروع دوره", headerKey: "billFrom" },
    { title: "پایان دوره", headerKey: "billTill" },
    {
      title: `قرائت شروع (${tag?.label ? renderUnit(tag.label, true) : ""})`,
      headerKey: "startBillNumber",
    },
    {
      title: `قرائت پایان (${tag?.label ? renderUnit(tag.label, true) : ""})`,
      headerKey: "endBillNumber",
    },
    {
      title: `میزان مصرف (${tag?.label ? renderUnit(tag.label, true) : ""})`,
      headerKey: "consumptions",
    },
    {
      title: `میانگین مصرف (${tag?.label ? renderUnit(tag.label, true) : ""})`,
      headerKey: "averageConsumption",
    },
    { title: "مبلغ قبض (ریال)", headerKey: "price" },
    { title: "مهلت پرداخت", headerKey: "deadLine" },
    { title: "مشاهده جزئیات", headerKey: "billActions" },
  ];
  const renderBillTable = () => {
    let billTableData: BillTableData[] = [];
    billsData?.data?.forEach((bill: BillObject) =>
      billTableData.push({
        billSerial: bill.bill_serial,
        billFrom: toPersianDate(bill.bill_start_date),
        // billTill: toPersianDate(bill.bill_end_date),
        billTill: toPersianDate(
          moment(bill.bill_end_date, "YYYY-M-D")
            .subtract(1, "day")
            .format("YYYY-M-D")
        ),
        startBillNumber: (
          bill.other_information.start_period_sum / 1000
        ).toLocaleString("fa-IR", {
          minimumFractionDigits: 3,
          maximumFractionDigits: 3,
        }),
        endBillNumber: (
          bill.other_information.end_period_sum / 1000
        ).toLocaleString("fa-IR", {
          minimumFractionDigits: 3,
          maximumFractionDigits: 3,
        }),
        consumptions: (bill.consumptions / 1000).toLocaleString("fa-IR", {
          minimumFractionDigits: 3,
          maximumFractionDigits: 3,
        }),
        averageConsumption: (
          (tag.label !== "گاز" ? bill.consumptions / 1000 : bill.consumptions) /
          bill.other_information.period_days
        ).toLocaleString("fa-IR", {
          minimumFractionDigits: 3,
          maximumFractionDigits: 3,
        }),
        price: bill.bill_price.toLocaleString("fa-IR", {
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        }),
        deadLine: toPersianDate(bill.payment_dead_line),
        billActions: renderBillActions(bill),
      })
    );
    return billTableData;
  };
  const renderCounterInfoTable = () => {
    let selectedCounter: DeviceObj[] = projectDeviceData.data.filter(
      (device: DeviceObj) => device.water_meter_serial === counter.value
    );
    let tableData = [
      {
        counterName: selectedCounter[0].water_meter_name,
        counterSerial: selectedCounter[0].water_meter_serial,
        counterType: selectedCounter[0].water_meter_type__water_meter_type_name,
        owner: `${selectedCounter[0].water_meter_user__user_name ?? "_"} ${
          selectedCounter[0].water_meter_user__user_lastname ?? "_"
        }`,
      },
    ];
    return tableData;
  };

  return (
    <div className="py-4">
      <CustomModal
        isOpen={isBillOpen}
        onClose={onBillClose}
        isBill={true}
        title={"قبض"}
        modalType="form"
        information={null}
        modalForm={
          <BillComponent
            billInfo={billInfo}
            onClose={onBillClose}
            patternSample={
              Array.isArray(patternData?.data) && patternData.data.length > 0
                ? patternData.data[0].pattern_list
                : []
            }
          />
        }
      />
      <BillSelectFilter
        filterPage="showBill"
        projectSelect={renderProjectSelectData()}
        tagSelect={renderTagSelectData()}
        counterSelect={renderCounterSelectData()}
        project={project}
        setProject={setProject}
        tag={tag}
        setTag={setTag}
        counter={counter}
        setCounter={setCounter}
      />
      {counter &&
      !projectDeviceIsLoading &&
      projectDeviceStatus === "success" ? (
        <SimpleTable
          header={counterInfoTableHeader}
          data={renderCounterInfoTable()}
        />
      ) : (
        <div className="py-2  text-navy-700  dark:text-white">
          دستگاه (کنتور) را انتخاب کنید !!!
        </div>
      )}
      {counter &&
      !billsIsLoading &&
      billsStatus === "success" &&
      !patternIsLoading &&
      patternStatus === "success" ? (
        <SimpleTable
          header={billsTableHeader}
          data={renderBillTable()}
          extra="h-[43vh]"
        />
      ) : (
        <>{counter ? <Loading /> : <></>}</>
      )}
    </div>
  );
};
export default ShowBillView;
