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

type Sequence_number struct {
	SqnScheme   string
	Sqn         string
	LastIndexes map[string]int32
	IndLength   int32
	DifSign     int32
}

func main() {
	fmt.Println("Hello client ...")

	opts := grpc.WithInsecure()
	cc, err := grpc.Dial("localhost:50051", opts)
	if err != nil {
		log.Fatal(err)
	}
	defer cc.Close()
	client := protos.NewPMNSubscriberConfigServicerClient(cc)
	var ktab = "AUTHSUBS"
	var algorithmId = "MILENAGE.1"
	sequence_val := Sequence_number{"NON_TIME_BASED", "000000000ac0", map[string]int32{}, 5, 0}
	var encOpcKey = "A3782F73B17811F4043EE66EBFD62519"
	var encTopcKey = "5E4AB35891375D2AEE812E67C309A629"
	var supi = "SUPI"
	request := PMNConverter(ktab, sequence_val, encOpcKey, encTopcKey, algorithmId, supi)
	client.PMNSubscriberConfig(context.Background(), request)
}

func PMNConverter(ktab string, sequence_num Sequence_number, encOpcKey string, encTopcKey string, algorithmId string, supi string) *protos.PMNSubscriberData {

	asd := &models.AuthenticationSubscription{
		KTAB:                  ktab,
		AuthenticationMethod:  &models.AuthMethod{},
		EncPermanentKey:       "",
		ProtectionParameterId: "none",
		SequenceNumber: &models.sequence_number{
			SqnScheme:   sequence_num.SqnScheme,
			Sqn:         sequence_num.Sqn,
			LastIndexes: sequence_num.LastIndexes,
			IndLength:   sequence_num.IndLength,
			DifSign:     sequence_num.DifSign,
		},
		AuthenticationManagementField: "8000",
		AlgorithmId:                   algorithmId,
		EncOpcKey:                     encOpcKey,
		EncTopcKey:                    encTopcKey,
		VectorGenerationInHss:         true,
		N5GcAuthMethod:                &models.AuthMethod{},
		RgAuthenticationInd:           true,
		Supi:                          supi,
	}
	return &protos.PMNSubscriberData{
		AuthSubsData: asd,
	}
}
