import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import { DynamicOption } from "components/fields/SelectInput";
import { useId } from "react";
import { MdAdd, MdDelete } from "react-icons/md";
import { reqFunction } from "utils/API";
import { renderUnit } from "utils/CommonFunctions";
import { renderToast, toEnglish } from "utils/globalUtils";

interface PatternFormFormProps {
  patternFromValue: null | string;
  setPatternFromValue: React.Dispatch<any>;
  patternToValue: null | string;
  setPatternToValue: React.Dispatch<any>;
  patternUnitPrice: null | string;
  setPatternUnitPrice: React.Dispatch<any>;
  tag: DynamicOption;
  isEditForm: boolean;
  patternId?: string;
  projectId?: string | any;
  onClose: Function;
  updateTable: any;
  patternList?: { k: string; v1: string; v2: string }[];
  setPatternList?: React.Dispatch<any>;
}
const PatternFrom = (props: PatternFormFormProps) => {
  const {
    patternFromValue,
    setPatternFromValue,
    patternToValue,
    setPatternToValue,
    patternUnitPrice,
    setPatternUnitPrice,
    tag,
    patternList,
    setPatternList,
    projectId,
    patternId,
    onClose,
    isEditForm,
    updateTable,
  } = props;
  const uniqId = useId();
  const renderRowInput = (pattern: { k: string; v1: string; v2: string }) => {
    return (
      <>
        <InputField
          id="tag-name"
          label={`مصرف از (${renderUnit(tag.label, true)})`}
          placeholder="حد پایین میزان مصرف را وارد کنید"
          type="text"
          defaultValue={pattern.v1}
        />
        <InputField
          id="tag-name"
          label={`مصرف تا (${renderUnit(tag.label, true)})`}
          placeholder="حد بالای میزان مصرف را وارد کنید"
          type="text"
          defaultValue={pattern.v2}
        />
        <InputField
          id="tag-name"
          label={`قیمت واحد (${renderUnit(tag.label, true)})`}
          placeholder="قیمت هر واحد را وارد کنید"
          type="text"
          defaultValue={pattern.k}
        />
      </>
    );
  };
  const renderActionbtns = (list: { k: string; v1: string; v2: string }[]) => {
    return (
      <div className=" flex items-center justify-end pb-2">
        <CustomButton
          onClick={() => {
            let new_list = [...patternList];
            new_list.pop();
            setPatternList(new_list);
          }}
          icon={<MdDelete />}
          color="red"
          extra="!p-2"
          isDisabled={list.length < 2 ? true : false}
        />
        <CustomButton
          onClick={() => {
            setPatternList([...patternList, { k: "", v1: "", v2: "" }]);
          }}
          icon={<MdAdd />}
          color="green"
          extra="!p-2"
        />
      </div>
    );
  };
  const createPattern = async () => {
    if (
      patternFromValue &&
      patternToValue &&
      patternUnitPrice &&
      !isNaN(Number(toEnglish(patternFromValue))) &&
      !isNaN(Number(toEnglish(patternToValue))) &&
      !isNaN(Number(toEnglish(patternUnitPrice)))
    ) {
      if (
        Number(toEnglish(patternFromValue)) < Number(toEnglish(patternToValue))
      ) {
        let response = await reqFunction("Pattern/admin/create", {
          pattern_tag: tag.value,
          pattern_project: projectId,
          pattern_list: [
            {
              k: patternUnitPrice,
              v1: patternFromValue,
              v2: patternToValue,
            },
          ],
        });
        if (response.code === 200) {
          renderToast("ایجاد الگوی مصرف با موفقیت انجام شد", "success");
          updateTable();
          onClose();
        } else {
          renderToast(
            response?.farsi_message
              ? response.farsi_message
              : "در ایجاد الگوی مصرف خطایی رخ داده",
            "err"
          );
        }
      } else {
        renderToast("ترتیب اعداد وارد شده صحیح نیست", "warn");
      }
    } else {
      renderToast("تمامی موارد را به صورت عدد وارد کنید", "warn");
    }
  };
  const editPattern = async () => {
    let list: { k: string; v1: string; v2: string }[] = [];
    document.querySelectorAll(".pattern-row").forEach((row) => {
      let inputs = row.querySelectorAll("input");
      let p = { k: "", v1: "", v2: "" };
      p.v1 = inputs[0].value;
      p.v2 = inputs[1].value;
      p.k = inputs[2].value;
      list.push(p);
    });
    let response = await reqFunction("Pattern/admin/edit", {
      pattern_id: patternId,
      pattern_tag: tag.value,
      pattern_project: projectId,
      pattern_list: list,
    });
    if (response.code === 200) {
      renderToast("تغییر الگوی مصرف با موفقیت انجام شد", "success");
      updateTable();
      onClose();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در تغییر الگوی مصرف خطایی رخ داده",
        "err"
      );
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      {!isEditForm ? (
        <div>
          <InputField
            id="tag-name"
            label={`مصرف از (${renderUnit(tag.label, true)})`}
            placeholder="حد پایین میزان مصرف را وارد کنید"
            type="text"
            state={patternFromValue}
            setState={setPatternFromValue}
          />
          <InputField
            id="tag-name"
            label={`مصرف تا (${renderUnit(tag.label, true)})`}
            placeholder="حد بالای میزان مصرف را وارد کنید"
            type="text"
            state={patternToValue}
            setState={setPatternToValue}
          />
          <InputField
            id="tag-name"
            label={`قیمت واحد (${renderUnit(tag.label, true)})`}
            placeholder="قیمت هر واحد را وارد کنید"
            type="text"
            state={patternUnitPrice}
            setState={setPatternUnitPrice}
          />
        </div>
      ) : (
        <div>
          {renderActionbtns(patternList)}
          {patternList.map((pattern, idx) => (
            <div
              key={uniqId + idx}
              className={`row-${idx + 1} pattern-row grid grid-cols-3 gap-4`}
            >
              {renderRowInput(pattern)}
            </div>
          ))}
        </div>
      )}

      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => (!isEditForm ? createPattern() : editPattern())}
          text={`${isEditForm ? "تغییر" : "ایجاد"}`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default PatternFrom;
