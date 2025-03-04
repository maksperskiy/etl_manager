import { Outlet } from "react-router";
import Header from "../../components/layout/Header/Header";

export default function MainLayout () {
    return <div className="etlm-main-layout">
      <Header />
      <div className="etlm-main-layout__container">
        <Outlet />
      </div>
    </div>
}
