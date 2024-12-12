interface UserProfile {
    username: string;
    image_url: string;
  }
  
  interface AppSidebarFooterProps {
    userProfile: UserProfile;
    handleLogout: () => void;
    router: any;
  }