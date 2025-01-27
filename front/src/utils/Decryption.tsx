import CryptoJS from "crypto-js";
export const decryptData = (
  encryptedData: string,
  key: string,
  url: string
): any => {
  try {
    // Decode the base64 encoded string
    const decodedData = CryptoJS.enc.Base64.parse(encryptedData);

    // Blowfish block size is 8 bytes (64 bits)
    const blockSize = 8;
    const ivSize = blockSize / 4;

    // Extract the IV
    const ivWords = decodedData.words.slice(0, ivSize);
    const iv = CryptoJS.lib.WordArray.create(ivWords, blockSize);

    // Extract the ciphertext
    const ciphertextWords = decodedData.words.slice(ivSize);
    const ciphertext = CryptoJS.lib.WordArray.create(
      ciphertextWords,
      decodedData.sigBytes - blockSize
    );

    // Decrypt the data using Blowfish algorithm
    const decryptedBytes = CryptoJS.Blowfish.decrypt(
      {
        ciphertext: ciphertext,
        salt: null,
      } as any, // Type assertion to bypass the type issue
      CryptoJS.enc.Utf8.parse(key),
      {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
      }
    );

    // Convert decrypted bytes to UTF-8 string
    const decryptedString = decryptedBytes.toString(CryptoJS.enc.Utf8);
    console.log("original message :", decryptedString);
    //fix diffrences in python and js
    const generalCorrection = decryptedString
      .replace(/'/g, '"')
      .replace(/\bNone\b/g, "null")
      .replace(/\bTrue\b/g, "true")
      .replace(/\bFalse\b/g, "false");
    // .replace(/UUID\("([^"]+)"\)/g, '"$1"');
    //some excludes
    const correctMessage =
      url === "WaterMeterProjectsURL/admin/total/statistics"
        ? generalCorrection.replace(/[()]/g, "")
        : generalCorrection;

    console.log(correctMessage);
    // Parse the decrypted string to JSON object
    const decryptedData = JSON.parse(correctMessage);
    // const decryptedData = JSON.parse(decryptedString);
    return decryptedData;
  } catch (error) {
    console.error("Error decrypting data:", error);
    throw new Error("Failed to decrypt data.");
  }
};
