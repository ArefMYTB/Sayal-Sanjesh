import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface TagFormProps {
  tagName: null | string;
  setTagName: React.Dispatch<any>;
  onClose: Function;
  updateTable: any;
}
const TagForm = (props: TagFormProps) => {
  const { tagName, setTagName, onClose, updateTable } = props;
  const createTag = async () => {
    // //console.log("tag name :", tagName);
    if (tagName) {
      const json = {
        water_meter_tag_name: tagName,
        water_meter_tag_other_information: {
          description: "",
        },
      };
      const data = new FormData();
      data.append("data", JSON.stringify(json));
      //   if (files.length > 0) {
      //     data.append("file", files[0]);
      //   }
      let response = await reqFunction("WaterMeterTags/admin/add", data);
      if (response.code === 200) {
        renderToast("ایجاد دسته با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        setTagName(null);
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ایجاد دسته خطایی رخ داده",
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
        id="tag-name"
        label="نام دسته"
        placeholder="نام دسته را وارد کنید"
        type="text"
        state={tagName}
        setState={setTagName}
      />

      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => createTag()}
          text={`ایجاد`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default TagForm;
