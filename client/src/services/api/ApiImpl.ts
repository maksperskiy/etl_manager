import ky from 'ky';
import ApiService from './Api';

const apiService = new ApiService(ky);

export default apiService;
