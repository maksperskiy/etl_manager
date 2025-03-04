import { Route, Routes } from "react-router";
import MainLayout from "./layout/MainLayout/MainLayout";
import DataBuilderView from "./views/DataBuilder/DataBuilder";
import DataSourcesView from "./views/DataSources/DataSources";
import LoginView from "./views/Login/Login";
import ManagerView from "./views/Manager/Manager";
import NotFoundView from "./views/NotFound/NotFound";
import RegisterView from "./views/Register/Register";

export default function Router() {
  return <Routes>
    <Route path="login" element={<LoginView />}></Route>
    <Route path="register" element={<RegisterView />}></Route>
    <Route element={<MainLayout />}>
      <Route path="/" element={<DataSourcesView />} />
      <Route path="data-sources" element={<DataSourcesView />} />
      <Route path="data-builder" element={<DataBuilderView />} />
      <Route path="manager" element={<ManagerView/>} />
    </Route>
    <Route path="*" element={<NotFoundView />}></Route>
  </Routes>
}
