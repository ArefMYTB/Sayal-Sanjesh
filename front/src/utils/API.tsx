import axios, { AxiosError } from "axios";
import { decryptData } from "./Decryption";

export const reqFunction = async (
  URL: string,
  Data: object,
  requestType: "get" | "post" = "post"
) => {
  const TOKEN = window.localStorage.getItem("token");
  try {
    if (TOKEN || URL === "admins/admin/login") {
      const config = {
        headers: {
          token: URL === "admins/admin/login" ? null : JSON.parse(TOKEN!),
        },
      };

      const response =
        requestType === "post"
          ? await axios.post(
              process.env.REACT_APP_SAYAL_API_ENDPOINT_MAIN + `/${URL}`,
              Data,
              config
            )
          : await axios.get(
              process.env.REACT_APP_SAYAL_API_ENDPOINT_MAIN + `/${URL}`,
              config
            );

      //decryption key
      const decryptionKey = "f675e6d9e84f419ba71b87a1fb57dfd5";

      // Check if the data field is encrypted and decrypt it
      let responseData = response.data;
      if (typeof responseData.data === "string") {
        responseData.data = decryptData(responseData.data, decryptionKey, URL);
      }

      return responseData;
    } else {
      return { code: 403, data: [] };
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError;
      if (axiosError.response) {
        console.log("Server responded with error:", axiosError.response.data);
        console.log("Status:", axiosError.response.status);
        console.log("Headers:", axiosError.response.headers);
        return axiosError.response.data;
      } else if (axiosError.request) {
        console.log(
          "Request made but no response received:",
          axiosError.request
        );
        return axiosError.response?.data;
      } else {
        console.log("Error setting up the request:", axiosError.message);
        return axiosError.response?.data;
      }
    } else {
      console.log("Unknown error occurred:", error);
    }
    throw error;
  }
};
