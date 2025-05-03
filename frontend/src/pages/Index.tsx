
import TravelBanner from "../components/TravelBanner";
import GroupChat from "../components/GroupChat";

const Index = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <TravelBanner />
        <GroupChat />
      </div>
    </div>
  );
};

export default Index;
