import { useState } from "react";
import FileUploader from "components/fields/ImageUpload";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";
import moment from "moment-jalaali";
import DatePicker from "react-datepicker2";

moment.loadPersian({ dialect: "persian-modern", usePersianDigits: false });

interface SnapshotFormProps {
  onClose: Function;
  serialnumber: string;
  refetchSnapshots: () => void;
  isEditMode?: boolean;
  snapshot?: any;
}

const SnapshotForm = (props: SnapshotFormProps) => {
  const { onClose, serialnumber, refetchSnapshots, isEditMode, snapshot } =
    props;
  const [watermeterId, setWatermeterId] = useState(serialnumber);
  const [createDate, setCreateDate] = useState(() =>
    snapshot?.create_time
      ? moment(snapshot.create_time, "YYYY-M-D HH:mm:ss")
      : moment().locale("fa")
  );
  const [createTime, setCreateTime] = useState(
    snapshot?.create_time
      ? moment(snapshot.create_time, "YYYY-M-D HH:mm:ss").format("HH:mm")
      : moment().format("HH:mm")
  );
  const [mechanicValue, setMechanicValue] = useState(
    snapshot?.mechanic_value || ""
  );
  // const [cumulativeValue, setCumulativeValue] = useState(
  //   snapshot?.cumulative_value || ""
  // );
  const [text, setText] = useState(snapshot?.text || "");
  const [imageUrl, setImageUrl] = useState<string | null>(
    snapshot?.image?.[0] || null
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!watermeterId) {
      renderToast("اطلاعات الزامی وارد نشده است", "warn");
      return;
    }

    // Convert Jalali date + time to Gregorian
    // Extract time from the input
    const [hour, minute] = createTime.split(":").map(Number);

    // Step 1: Set the time on the Jalali moment
    const jalaliWithTime = createDate.clone().set({
      hour,
      minute,
      second: 0,
      millisecond: 0,
    });
    // Step 2: Convert to Gregorian properly
    const gregorian = moment(
      jalaliWithTime.format("jYYYY/jMM/jDD HH:mm"),
      "jYYYY/jMM/jDD HH:mm"
    );
    // Final values to send to Django
    const create_date = gregorian.format("YYYY-MM-DD"); // e.g., "2025-05-05"
    const create_time = gregorian.format("HH:mm");

    const payload = {
      watermeter_id: watermeterId,
      create_date: create_date,
      create_time: create_time,
      mechanic_value: parseFloat(mechanicValue),
      // cumulative_value: parseFloat(cumulativeValue),
      text,
      image: [imageUrl], // Expecting array in backend
    };

    const endpoint = isEditMode
      ? "snapshots/admin/edit"
      : "snapshots/admin/create";

    const response = await reqFunction(endpoint, payload);

    if (response.code === 200) {
      renderToast("ثبت با موفقیت انجام شد", "success");
      // Optionally reset the form
      setWatermeterId("");
      // setCreateDate("");
      setCreateTime("");
      setMechanicValue("");
      // setCumulativeValue("");
      setText("");
      setImageUrl(null);
      // Close form and refresh table
      onClose();
      refetchSnapshots();
    } else {
      renderToast(response.farsi_message || "خطا در ثبت", "err");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block">شماره سریال کنتور</label>
        <input
          type="text"
          value={watermeterId}
          onChange={(e) => setWatermeterId(e.target.value)}
          className="w-full rounded border p-2"
          disabled={isEditMode}
        />
      </div>
      {!isEditMode ? (
        <div>
          <label className="block">تاریخ ایجاد</label>
          <DatePicker
            isGregorian={false}
            value={createDate}
            onChange={(value) => setCreateDate(value)}
            timePicker={false}
            inputFormat="jYYYY/jMM/jDD"
          />
        </div>
      ) : (
        <div>
          <label className="block">تاریخ ایجاد</label>
          <input
            type="text"
            value={createDate.format("jYYYY/jMM/jDD")}
            className="w-full rounded border p-2 text-left"
            disabled={isEditMode}
          />
        </div>
      )}
      <div>
        <label className="block">زمان ایجاد</label>
        <input
          type="time"
          value={createTime}
          onChange={(e) => setCreateTime(e.target.value)}
          className="w-full rounded border p-2"
          disabled={isEditMode}
        />
      </div>
      <div>
        <label className="block">مقدار مکانیکی (لیتر)</label>
        <input
          type="number"
          value={mechanicValue}
          onChange={(e) => setMechanicValue(e.target.value)}
          className="w-full rounded border p-2"
        />
      </div>
      {/* <div>
        <label className="block">مقدار تجمعی</label>
        <input
          type="number"
          value={cumulativeValue}
          onChange={(e) => setCumulativeValue(e.target.value)}
          className="w-full rounded border p-2"
          disabled={isEditMode}
        />
      </div> */}
      <div>
        <label className="block">توضیحات</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full rounded border p-2"
        ></textarea>
      </div>
      {!isEditMode ? (
        <div>
          <label className="block">تصویر</label>
          <FileUploader
            preview={imageUrl}
            setPreview={setImageUrl}
            uploaderType="projectImage"
            uploadEndpoint="snapshots/admin/upload"
          />
        </div>
      ) : (
        <div>
          <label className="block">تصویر</label>
          {imageUrl && (
            <div className="mb-2">
              <img
                src={imageUrl}
                alt="ویرایش عکس"
                className="h-48 w-48 rounded border object-cover"
              />
            </div>
          )}
        </div>
      )}
      <button
        type="submit"
        className="w-full rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
      >
        ثبت برداشت
      </button>
    </form>
  );
};

export default SnapshotForm;
