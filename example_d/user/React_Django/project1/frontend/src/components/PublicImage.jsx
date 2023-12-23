//import pic from "../assets_in_public_dir/images/mercury_public.jpg"; // lo toma directamente del dir public, es un seteo de webpack
// https://stackoverflow.com/questions/44114436/the-create-react-app-imports-restriction-outside-of-src-directory
import pic from "../images/mercury_public.jpg";
function PublicImage(){
 return <img src={pic} />
}
export default PublicImage;