/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** foodEnum */
export enum FoodEnum {
  Fruits = "fruits",
  Vegetables = "vegetables",
  Dairy = "dairy",
}

/** TagName */
export enum TagName {
  Express = "express",
  Standard = "standard",
  Fragile = "fragile",
  Heavy = "heavy",
  International = "international",
  Domestic = "domestic",
  TemperatureControlled = "temperature_controlled",
  Gift = "gift",
  Return = "return",
  Documents = "documents",
}

/** ShipmentStatus */
export enum ShipmentStatus {
  Placed = "placed",
  InTransit = "in_transit",
  OutForDelivery = "out_for_delivery",
  Delivered = "delivered",
  Cancelled = "cancelled",
}

/** Body_login_delivery_partner */
export interface BodyLoginDeliveryPartner {
  /** Grant Type */
  grant_type?: string | null;
  /** Username */
  username: string;
  /** Password */
  password: string;
  /**
   * Scope
   * @default ""
   */
  scope?: string;
  /** Client Id */
  client_id?: string | null;
  /** Client Secret */
  client_secret?: string | null;
}

/** Body_login_seller */
export interface BodyLoginSeller {
  /** Grant Type */
  grant_type?: string | null;
  /** Username */
  username: string;
  /** Password */
  password: string;
  /**
   * Scope
   * @default ""
   */
  scope?: string;
  /** Client Id */
  client_id?: string | null;
  /** Client Secret */
  client_secret?: string | null;
}

/** Body_reset_password */
export interface BodyResetPassword {
  /** Password */
  password: string;
}

/** Body_submit_review */
export interface BodySubmitReview {
  /**
   * Rating
   * @min 1
   * @max 5
   */
  rating: number;
  /** Comment */
  comment: string | null;
}

/**
 * BookRequest
 * @example {"author":"Who knows who I am","description":"A book about spooky girl inside a castle with magic wand","rating":5,"title":"Vampire Dairy"}
 */
export interface BookRequest {
  /** Id */
  id?: number | null;
  /**
   * Title
   * @minLength 2
   */
  title: string;
  /**
   * Author
   * @minLength 2
   */
  author: string;
  /**
   * Description
   * @minLength 2
   * @maxLength 200
   */
  description: string;
  /**
   * Rating
   * @exclusiveMin 0
   * @exclusiveMax 6
   */
  rating: number;
}

/** CreatePostIn */
export interface CreatePostIn {
  /** Title */
  title: string;
  /** Content */
  content: string;
}

/** DeliveryPartnerCreate */
export interface DeliveryPartnerCreate {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /** Serviceable Zip Codes */
  serviceable_zip_codes: number[];
  /** Max Handling Capacity */
  max_handling_capacity: number;
  /** Password */
  password: string;
}

/** DeliveryPartnerRead */
export interface DeliveryPartnerRead {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /** Serviceable Zip Codes */
  serviceable_zip_codes: number[];
  /** Max Handling Capacity */
  max_handling_capacity: number;
}

/** DeliveryPartnerUpdate */
export interface DeliveryPartnerUpdate {
  /** Serviceable Zip Codes */
  serviceable_zip_codes?: number[] | null;
  /** Max Handling Capacity */
  max_handling_capacity?: number | null;
}

/** Example */
export interface Example {
  /** Content */
  content: string;
}

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/** SellerCreate */
export interface SellerCreate {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /** Password */
  password: string;
}

/** SellerRead */
export interface SellerRead {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
}

/** Shipment */
export interface Shipment {
  /**
   * Id
   * @format uuid
   */
  id?: string;
  /** Content */
  content: string;
  /**
   * Weight
   * @max 25
   */
  weight: number;
  /** Destination */
  destination: number;
  /**
   * Estimated Delivery
   * @format date-time
   */
  estimated_delivery: string;
  /**
   * Created At
   * @format date-time
   */
  created_at: string;
  /**
   * Client Contact Email
   * @format email
   */
  client_contact_email: string;
  /** Client Contact Phone */
  client_contact_phone: number | null;
  /**
   * Seller Id
   * @format uuid
   */
  seller_id: string;
  /**
   * Delivery Partner Id
   * @format uuid
   */
  delivery_partner_id: string;
}

/** ShipmentCreate */
export interface ShipmentCreate {
  /** Content */
  content: string;
  /**
   * Weight
   * @max 25
   */
  weight: number;
  /** Destination */
  destination: number;
  /**
   * Client Contact Email
   * @format email
   */
  client_contact_email: string;
  /** Client Contact Phonel */
  client_contact_phonel?: number | null;
}

/** ShipmentEvent */
export interface ShipmentEvent {
  /**
   * Id
   * @format uuid
   */
  id: string;
  /**
   * Created At
   * @format date-time
   */
  created_at: string;
  /** Location */
  location: number;
  status: ShipmentStatus;
  /** Description */
  description?: string | null;
  /**
   * Shipment Id
   * @format uuid
   */
  shipment_id: string;
}

/** ShipmentRead */
export interface ShipmentRead {
  /** Content */
  content: string;
  /**
   * Weight
   * @max 25
   */
  weight: number;
  /** Destination */
  destination: number;
  /**
   * Id
   * @format uuid
   */
  id: string;
  /** Estimated Delivery */
  estimated_delivery?: string | null;
  /** Timeline */
  timeline: ShipmentEvent[];
  /** Tags */
  tags: Tag[];
}

/** ShipmentUpdate */
export interface ShipmentUpdate {
  /** Content */
  content?: string | null;
  /** Weight */
  weight?: number | null;
  /** Location */
  location?: number | null;
  /** Description */
  description?: string | null;
  status: ShipmentStatus;
  /** Estimated Delivery */
  estimated_delivery?: string | null;
}

/** Tag */
export interface Tag {
  /**
   * Id
   * @format uuid
   */
  id: string;
  name: TagName;
  /** Instruction */
  instruction: string;
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
}

import type {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  HeadersDefaults,
  ResponseType,
} from "axios";
import axios from "axios";

export type QueryParamsType = Record<string | number, any>;

export interface FullRequestParams
  extends Omit<AxiosRequestConfig, "data" | "params" | "url" | "responseType"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseType;
  /** request body */
  body?: unknown;
}

export type RequestParams = Omit<
  FullRequestParams,
  "body" | "method" | "query" | "path"
>;

export interface ApiConfig<SecurityDataType = unknown>
  extends Omit<AxiosRequestConfig, "data" | "cancelToken"> {
  securityWorker?: (
    securityData: SecurityDataType | null,
  ) => Promise<AxiosRequestConfig | void> | AxiosRequestConfig | void;
  secure?: boolean;
  format?: ResponseType;
}

export enum ContentType {
  Json = "application/json",
  JsonApi = "application/vnd.api+json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public instance: AxiosInstance;
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private secure?: boolean;
  private format?: ResponseType;

  constructor({
    securityWorker,
    secure,
    format,
    ...axiosConfig
  }: ApiConfig<SecurityDataType> = {}) {
    this.instance = axios.create({
      ...axiosConfig,
      baseURL: axiosConfig.baseURL || "",
    });
    this.secure = secure;
    this.format = format;
    this.securityWorker = securityWorker;
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected mergeRequestParams(
    params1: AxiosRequestConfig,
    params2?: AxiosRequestConfig,
  ): AxiosRequestConfig {
    const method = params1.method || (params2 && params2.method);

    return {
      ...this.instance.defaults,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...((method &&
          this.instance.defaults.headers[
            method.toLowerCase() as keyof HeadersDefaults
          ]) ||
          {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected stringifyFormItem(formItem: unknown) {
    if (typeof formItem === "object" && formItem !== null) {
      return JSON.stringify(formItem);
    } else {
      return `${formItem}`;
    }
  }

  protected createFormData(input: Record<string, unknown>): FormData {
    if (input instanceof FormData) {
      return input;
    }
    return Object.keys(input || {}).reduce((formData, key) => {
      const property = input[key];
      const propertyContent: any[] =
        property instanceof Array ? property : [property];

      for (const formItem of propertyContent) {
        const isFileType = formItem instanceof Blob || formItem instanceof File;
        formData.append(
          key,
          isFileType ? formItem : this.stringifyFormItem(formItem),
        );
      }

      return formData;
    }, new FormData());
  }

  public request = async <T = any, _E = any>({
    secure,
    path,
    type,
    query,
    format,
    body,
    ...params
  }: FullRequestParams): Promise<AxiosResponse<T>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const responseFormat = format || this.format || undefined;

    if (
      type === ContentType.FormData &&
      body &&
      body !== null &&
      typeof body === "object"
    ) {
      body = this.createFormData(body as Record<string, unknown>);
    }

    if (
      type === ContentType.Text &&
      body &&
      body !== null &&
      typeof body !== "string"
    ) {
      body = JSON.stringify(body);
    }

    return this.instance.request({
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type ? { "Content-Type": type } : {}),
      },
      params: query,
      responseType: responseFormat,
      data: body,
      url: path,
    });
  };
}

/**
 * @title Ventuno API
 * @version 1.0.0
 *
 * API for managing sellers, delivery partners, shipments, and more.
 */
export class Api<
  SecurityDataType extends unknown,
> extends HttpClient<SecurityDataType> {
  healthy = {
    /**
     * No description
     *
     * @name HealthCheck
     * @summary Health Check
     * @request GET:/healthy
     * @secure
     */
    healthCheck: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/healthy`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),
  };
  healthy2 = {
    /**
     * No description
     *
     * @name HealthCheck2
     * @summary Health Check2
     * @request GET:/healthy2
     * @secure
     */
    healthCheck2: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/healthy2`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),
  };
  seller = {
    /**
     * No description
     *
     * @tags seller
     * @name RegisterSeller
     * @summary Register Seller
     * @request POST:/seller/signup
     * @secure
     */
    registerSeller: (data: SellerCreate, params: RequestParams = {}) =>
      this.request<SellerRead, HTTPValidationError>({
        path: `/seller/signup`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags seller
     * @name LoginSeller
     * @summary Login Seller
     * @request POST:/seller/token
     * @secure
     */
    loginSeller: (data: BodyLoginSeller, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/token`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags seller
     * @name VerifySellerEmail
     * @summary Verify Seller Email
     * @request GET:/seller/verify
     * @secure
     */
    verifySellerEmail: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/verify`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags seller
     * @name ForgotPassword
     * @summary Forgot Password
     * @request GET:/seller/forgot_password
     * @secure
     */
    forgotPassword: (
      query: {
        /**
         * Email
         * @format email
         */
        email: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/forgot_password`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags seller
     * @name GetResetPasswordForm
     * @summary Get Reset Password Form
     * @request GET:/seller/reset_password_form
     * @secure
     */
    getResetPasswordForm: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/reset_password_form`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags seller
     * @name ResetPassword
     * @summary Reset Password
     * @request POST:/seller/reset_password
     * @secure
     */
    resetPassword: (
      query: {
        /** Token */
        token: string;
      },
      data: BodyResetPassword,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/reset_password`,
        method: "POST",
        query: query,
        body: data,
        secure: true,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * @description Now dashboard will be token authenticated
     *
     * @tags seller
     * @name GetDashboard
     * @summary Get Dashboard
     * @request GET:/seller/dashboard
     * @secure
     */
    getDashboard: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/seller/dashboard`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags seller
     * @name LogoutSeller
     * @summary Logout Seller
     * @request GET:/seller/logout
     * @secure
     */
    logoutSeller: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/seller/logout`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Now dashboard will be token authenticated
     *
     * @tags seller
     * @name GetDashboardv2
     * @summary Get Dashboardv2
     * @request GET:/seller/dashboardv2
     * @secure
     */
    getDashboardv2: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/seller/dashboardv2`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),
  };
  partner = {
    /**
     * No description
     *
     * @tags Delivery Partner, Delivery Partner
     * @name RegisterDeliveryPartner
     * @summary Register Delivery Partner
     * @request POST:/partner/signup
     * @secure
     */
    registerDeliveryPartner: (
      data: DeliveryPartnerCreate,
      params: RequestParams = {},
    ) =>
      this.request<DeliveryPartnerRead, HTTPValidationError>({
        path: `/partner/signup`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner, Delivery Partner
     * @name LoginDeliveryPartner
     * @summary Login Delivery Partner
     * @request POST:/partner/token
     * @secure
     */
    loginDeliveryPartner: (
      data: BodyLoginDeliveryPartner,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partner/token`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner, Delivery Partner
     * @name VerifyDeliveryPartnerEmail
     * @summary Verify Delivery Partner Email
     * @request GET:/partner/verify
     * @secure
     */
    verifyDeliveryPartnerEmail: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partner/verify`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner, Delivery Partner
     * @name ForgotPassword
     * @summary Forgot Password
     * @request GET:/partner/forgot_password
     * @secure
     */
    forgotPassword: (
      query: {
        /**
         * Email
         * @format email
         */
        email: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partner/forgot_password`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner, Delivery Partner
     * @name GetResetPasswordForm
     * @summary Get Reset Password Form
     * @request GET:/partner/reset_password_form
     * @secure
     */
    getResetPasswordForm: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partner/reset_password_form`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner, Delivery Partner
     * @name ResetPassword
     * @summary Reset Password
     * @request POST:/partner/reset_password
     * @secure
     */
    resetPassword: (
      query: {
        /** Token */
        token: string;
      },
      data: BodyResetPassword,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partner/reset_password`,
        method: "POST",
        query: query,
        body: data,
        secure: true,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * @description Update data with given fields uses Pydantic’s model_dump() method to convert the partner_update object (likely a BaseModel) into a plain Python dict. The key part is: exclude_none=True — What It Does? It tells Pydantic to exclude any fields where the value is None from the output dictionary.
     *
     * @tags Delivery Partner, Delivery Partner, Delivery Partner
     * @name UpdateDeliveryPartner
     * @summary Update Delivery Partner
     * @request POST:/partner/update
     * @secure
     */
    updateDeliveryPartner: (
      data: DeliveryPartnerUpdate,
      params: RequestParams = {},
    ) =>
      this.request<DeliveryPartnerRead, HTTPValidationError>({
        path: `/partner/update`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner, Delivery Partner
     * @name LogoutDeliveryPartner
     * @summary Logout Delivery Partner
     * @request GET:/partner/logout
     * @secure
     */
    logoutDeliveryPartner: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/partner/logout`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),
  };
  shipmentv3 = {
    /**
     * No description
     *
     * @tags shipment v3
     * @name GetTracking
     * @summary Get Tracking
     * @request GET:/shipmentv3/track
     * @secure
     */
    getTracking: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/shipmentv3/track`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name GetShipment
     * @summary Get Shipment
     * @request GET:/shipmentv3/
     * @secure
     */
    getShipment: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipmentv3/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description why we dont use below sentence and we face an error: # return await ShipmentService(service).add(shipment) Instead of calling service.add(shipment) directly, it creates a new ShipmentService instance with ShipmentService(service).
     *
     * @tags shipment v3
     * @name SubmitShipment
     * @summary Submit Shipment
     * @request POST:/shipmentv3/
     * @secure
     */
    submitShipment: (data: ShipmentCreate, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/shipmentv3/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name UpdateShipment
     * @summary Update Shipment
     * @request PATCH:/shipmentv3/
     * @secure
     */
    updateShipment: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      data: ShipmentUpdate,
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipmentv3/`,
        method: "PATCH",
        query: query,
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name GetShipmentv2
     * @summary Get Shipmentv2
     * @request GET:/shipmentv3/v2/
     * @secure
     */
    getShipmentv2: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipmentv3/v2/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Add new **shipment**
     *
     * @tags shipment v3
     * @name AddNewShipment
     * @summary Add New **Shipment**
     * @request POST:/shipmentv3/v2/
     * @secure
     */
    addNewShipment: (data: ShipmentCreate, params: RequestParams = {}) =>
      this.request<Shipment, HTTPValidationError>({
        path: `/shipmentv3/v2/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name UpdateShipmentv2
     * @summary Update Shipmentv2
     * @request PATCH:/shipmentv3/v2
     * @secure
     */
    updateShipmentv2: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      data: ShipmentUpdate,
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipmentv3/v2`,
        method: "PATCH",
        query: query,
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name GetShipmentsWithSpecificTag
     * @summary Get Shipments With Specific Tag
     * @request GET:/shipmentv3/tagged
     * @secure
     */
    getShipmentsWithSpecificTag: (
      query: {
        tag_name: TagName;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead[], HTTPValidationError>({
        path: `/shipmentv3/tagged`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name AddTagToShipment
     * @summary Add Tag To Shipment
     * @request GET:/shipmentv3/tag
     * @secure
     */
    addTagToShipment: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
        tag_name: TagName;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipmentv3/tag`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name RemoveTagFromShipment
     * @summary Remove Tag From Shipment
     * @request DELETE:/shipmentv3/tag
     * @secure
     */
    removeTagFromShipment: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
        tag_name: TagName;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipmentv3/tag`,
        method: "DELETE",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name CancelShipment
     * @summary Cancel Shipment
     * @request GET:/shipmentv3/cancel
     * @secure
     */
    cancelShipment: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<Shipment, HTTPValidationError>({
        path: `/shipmentv3/cancel`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name CancelShipmentv2
     * @summary Cancel Shipmentv2
     * @request GET:/shipmentv3/cancel/v2
     * @secure
     */
    cancelShipmentv2: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipmentv3/cancel/v2`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name SubmitReviewPage
     * @summary Submit Review Page
     * @request GET:/shipmentv3/review
     * @secure
     */
    submitReviewPage: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/shipmentv3/review`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags shipment v3
     * @name SubmitReview
     * @summary Submit Review
     * @request POST:/shipmentv3/review
     * @secure
     */
    submitReview: (
      query: {
        /** Token */
        token: string;
      },
      data: BodySubmitReview,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/shipmentv3/review`,
        method: "POST",
        query: query,
        body: data,
        secure: true,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),
  };
  test = {
    /**
     * No description
     *
     * @tags test
     * @name AllBooks
     * @summary All Books
     * @request GET:/test/books
     * @secure
     */
    allBooks: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/test/books`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name SingleBook
     * @summary Single Book
     * @request GET:/test/books/{book_id}
     * @secure
     */
    singleBook: (bookId: number, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/test/books/${bookId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name DeleteBook
     * @summary Delete Book
     * @request DELETE:/test/books/{book_id}
     * @secure
     */
    deleteBook: (bookId: number, params: RequestParams = {}) =>
      this.request<void, HTTPValidationError>({
        path: `/test/books/${bookId}`,
        method: "DELETE",
        secure: true,
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name ReadBooksByRating
     * @summary Read Books By Rating
     * @request GET:/test/books/
     * @secure
     */
    readBooksByRating: (
      query: {
        /**
         * Rating
         * @exclusiveMin 0
         * @exclusiveMax 6
         */
        rating: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/test/books/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description This endpoint is based on Python class & It will not show SCHEMA in body of Swagger
     *
     * @tags test
     * @name CreateBook
     * @summary Create Book
     * @request POST:/test/create-book
     * @secure
     */
    createBook: (data: any, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/test/create-book`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description This endpoint validation is based on Pydantic model & It will show Schema in body of Swagger
     *
     * @tags test
     * @name CreateBook2
     * @summary Create Book2
     * @request POST:/test/create-book2
     * @secure
     */
    createBook2: (data: BookRequest, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/test/create-book2`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Description of this function
     *
     * @tags test
     * @name Root
     * @summary Root
     * @request GET:/test/
     * @deprecated
     * @secure
     */
    root: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/test/`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name GetFood
     * @summary Get Food
     * @request GET:/test/foods/{food_name}
     * @secure
     */
    getFood: (foodName: FoodEnum, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/test/foods/${foodName}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name ListItems
     * @summary List Items
     * @request GET:/test/items/
     * @secure
     */
    listItems: (
      query?: {
        /**
         * Skip
         * @default 0
         */
        skip?: number;
        /**
         * Limit
         * @default 10
         */
        limit?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/test/items/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name CreatePost
     * @summary Create Post
     * @request POST:/test/create/
     * @secure
     */
    createPost: (data: CreatePostIn, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/test/create/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description x => is a QUERY parameter & is not optioanl, it has to be sent in URL y => is a PATH parameter & is not optioanl, it has to be sent in URL z => is a QUERY parameter & is  optioanl, & if you want you can dont send it in url
     *
     * @tags test
     * @name Xyz
     * @summary Xyz
     * @request POST:/test/path/{y}
     * @secure
     */
    xyz: (
      y: string,
      query: {
        /** X */
        x: number;
        /** Z */
        z?: number | null;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/test/path/${y}`,
        method: "POST",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description x => is a QUERY parameter & is not optioanl, it has to be sent in URL y => is a PATH parameter & is not optioanl, it has to be sent in URL z => is a QUERY parameter & is  optioanl, & if you want you can dont send it in url my_body => Post method can have a body(But get method cannot have a body), here body is not optional
     *
     * @tags test
     * @name XyzWithBody
     * @summary Xyz With Body
     * @request POST:/test/path2/{y}
     * @secure
     */
    xyzWithBody: (
      y: string,
      query: {
        /** X */
        x: number;
        /** Z */
        z?: number | null;
      },
      data: any,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/test/path2/${y}`,
        method: "POST",
        query: query,
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description x => is a QUERY parameter & is not optioanl, it has to be sent in URL y => is a PATH parameter & is not optioanl, it has to be sent in URL z => is a QUERY parameter & is  optioanl, & if you want you can dont send it in url my_body => Post method can have a body(But get method cannot have a body), here body is optional
     *
     * @tags test
     * @name XyzWithOptionalBody
     * @summary Xyz With Optional Body
     * @request POST:/test/path3/{y}
     * @secure
     */
    xyzWithOptionalBody: (
      y: string,
      query: {
        /** X */
        x: number;
        /** Z */
        z?: number | null;
      },
      data: any,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/test/path3/${y}`,
        method: "POST",
        query: query,
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name GetShipment
     * @summary Get Shipment
     * @request GET:/test/shipment
     * @secure
     */
    getShipment: (
      query: {
        /** Id */
        id: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/test/shipment`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name SubmitShipment
     * @summary Submit Shipment
     * @request POST:/test/shipment
     * @secure
     */
    submitShipment: (data: ShipmentCreate, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/test/shipment`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name UpdateShipment
     * @summary Update Shipment
     * @request PATCH:/test/shipment
     * @secure
     */
    updateShipment: (
      query: {
        /** Id */
        id: number;
      },
      data: ShipmentUpdate,
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/test/shipment`,
        method: "PATCH",
        query: query,
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name DeleteShipment
     * @summary Delete Shipment
     * @request DELETE:/test/shipment
     * @secure
     */
    deleteShipment: (
      query: {
        /** Id */
        id: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<Record<string, string>, HTTPValidationError>({
        path: `/test/shipment`,
        method: "DELETE",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name SubmitShipment1
     * @summary Submit Shipment1
     * @request POST:/test/shipment1
     * @secure
     */
    submitShipment1: (data: ShipmentCreate, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/test/shipment1`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name SubmitShipment2
     * @summary Submit Shipment2
     * @request POST:/test/shipment2
     * @secure
     */
    submitShipment2: (data: Record<string, any>, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/test/shipment2`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name SubmitShipment3
     * @summary Submit Shipment3
     * @request POST:/test/shipment3
     * @secure
     */
    submitShipment3: (
      query: {
        /** Shipment */
        shipment: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/test/shipment3`,
        method: "POST",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags test
     * @name SubmitShipment4
     * @summary Submit Shipment4
     * @request POST:/test/shipment4
     * @secure
     */
    submitShipment4: (data: Example, params: RequestParams = {}) =>
      this.request<any, HTTPValidationError>({
        path: `/test/shipment4`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),
  };
}
