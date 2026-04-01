import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import en from "./en.json";
import da from "./da.json";
import it from "./it.json";

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    da: { translation: da },
    it: { translation: it },
  },
  lng: localStorage.getItem("language") || "en",
  fallbackLng: "en",
  interpolation: {
    escapeValue: false,
  },
});

export default i18n;
