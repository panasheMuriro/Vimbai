import { FC } from "react";
import BlogList from "./components/BlogList";
import Header from "./components/Header";
import Bio from "./components/Bio";

const App: FC = () => {
  return (
    <>
      <Header />
     <Bio/>
      <BlogList />
    </>
  );
};

export default App;
