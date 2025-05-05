import { useState } from "react";
import FileUploader from "components/fields/ImageUpload";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

const SnapshotForm = () => {
  const [watermeterId, setWatermeterId] = useState("");
  const [mechanicValue, setMechanicValue] = useState("");
  const [cumulativeValue, setCumulativeValue] = useState("");
  const [text, setText] = useState("");
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!watermeterId) {
      renderToast("اطلاعات الزامی وارد نشده است", "warn");
      return;
    }

    const payload = {
      watermeter_id: watermeterId,
      mechanic_value: parseFloat(mechanicValue),
      cumulative_value: parseFloat(cumulativeValue),
      text,
      image: [imageUrl], // Expecting array in backend
    };

    const response = await reqFunction("snapshots/admin/create", payload);

    if (response.code === 200) {
      renderToast("ثبت با موفقیت انجام شد", "success");
      // Optionally reset the form
      setWatermeterId("");
      setMechanicValue("");
      setCumulativeValue("");
      setText("");
      setImageUrl(null);
    } else {
      renderToast(response.farsi_message || "خطا در ثبت", "err");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="mx-auto max-w-md space-y-4 rounded bg-white p-4 shadow"
    >
      <div>
        <label className="block">شناسه کنتور آب</label>
        <input
          type="text"
          value={watermeterId}
          onChange={(e) => setWatermeterId(e.target.value)}
          className="w-full rounded border p-2"
        />
      </div>

      <div>
        <label className="block">مقدار مکانیکی</label>
        <input
          type="number"
          value={mechanicValue}
          onChange={(e) => setMechanicValue(e.target.value)}
          className="w-full rounded border p-2"
        />
      </div>

      <div>
        <label className="block">مقدار تجمعی</label>
        <input
          type="number"
          value={cumulativeValue}
          onChange={(e) => setCumulativeValue(e.target.value)}
          className="w-full rounded border p-2"
        />
      </div>

      <div>
        <label className="block">توضیحات</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full rounded border p-2"
        ></textarea>
      </div>

      <div>
        <label className="block">تصویر</label>
        <FileUploader
          preview={imageUrl}
          setPreview={setImageUrl}
          uploaderType="projectImage"
          uploadEndpoint="snapshots/admin/upload"
        />
      </div>

      <button
        type="submit"
        className="w-full rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
      >
        ثبت عکس‌برداری
      </button>
    </form>
  );
};

export default SnapshotForm;
