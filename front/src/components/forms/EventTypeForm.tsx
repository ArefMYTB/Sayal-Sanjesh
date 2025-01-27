import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface EventTypeFormProps {
  importanceSelectData?: DynamicOption[] | null;
  importance: DynamicOption | null;
  setImportance: React.Dispatch<any>;
  eventTypeName: null | string;
  setEventTypeName: React.Dispatch<any>;
  onClose: Function;
  updateTable: any;
}
const EventTypeForm = (props: EventTypeFormProps) => {
  const {
    importanceSelectData,
    importance,
    setImportance,
    eventTypeName,
    setEventTypeName,
    onClose,
    updateTable,
  } = props;
  const createEventType = async () => {
    if (importance && eventTypeName) {
      let response = await reqFunction("EventType/admin/create", {
        event_type_keyword: eventTypeName,
        event_type_importance: importance.value,
        evnet_type_information: {},
      });
      if (response.code === 200) {
        renderToast("ایجاد نوع رخداد با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        setEventTypeName("");
        setImportance(null);
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ایجاد نوع رخداد خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      <InputField
        id="device-type-name"
        label="نام نوع رخداد"
        placeholder="نام نوع رخداد را وارد کنید"
        type="text"
        state={eventTypeName}
        setState={setEventTypeName}
      />
      <SelectInput
        label="اهمیت رخداد"
        placeholder="میزان اهمیت رخداد را انتخاب کنید"
        dynamicOptions={importanceSelectData}
        state={importance}
        setState={setImportance}
      />
      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => createEventType()}
          text={`ایجاد نوع رخداد`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default EventTypeForm;
