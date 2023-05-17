package main

import (
	"context"
	"fmt"
	protos "magma/lte/cloud/go/protos"
	models "magma/lte/cloud/go/protos/models"

	"google.golang.org/grpc"

	//"github.com/go-openapi/swag"
	"log"
)

func main() {
	fmt.Println("Hello client ...")

	opts := grpc.WithInsecure()
	cc, err := grpc.Dial("localhost:50051", opts)
	if err != nil {
		log.Fatal(err)
	}
	defer cc.Close()

	client := protos.NewPMNSubscriberServiceClient(cc)
	request := &protos.PMNSubscriberData{
		auth_subs_data: &models.AuthenticationSubscription{
			KTAB:                  "AUTHSUBS",
			AuthenticationMethod:  &models.AuthMethod{},
			EncPermanentKey:       "",
			ProtectionParameterId: "none",
			SequenceNumber: &models.sequence_number{
				SqnScheme: "NON_TIME_BASED",
				Sqn:       "000000000ac0",
				LastIndexes: map[string]int32{
					"ausf": 22,
				},
				IndLength: 5,
				DifSign:   "POSITIVE",
			},
			AuthenticationManagementField: "8000",
			AlgorithmId:                   "MILENAGE.1",
			EncOpcKey:                     "A3782F73B17811F4043EE66EBFD62519",
			EncTopcKey:                    "5E4AB35891375D2AEE812E67C309A629",
			VectorGenerationInHss:         true,
			N5GcAuthMethod:                &models.AuthMethod{},
			RgAuthenticationInd:           true,
			Supi:                          "SUPI",
		},
	}

	client.PMNSubscriberConfig(context.Background(), request)
}
